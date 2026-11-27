#!/usr/bin/env python3
"""
Generate voice-cloned narration audio for each scene using local F5-TTS
(F5TTS_v1_Base) with the student's pre-processed voice reference (voice_ref.wav),
falling back to edge-tts only if requested or unavailable.

Each scene's audio is time-synchronized to match the exact duration of its
rendered Manim scene MP4, silence-trimmed gently, loudness-normalized (-16 LUFS),
and exported at 48 kHz stereo.

Usage:
    source venv/bin/activate
    python _Code/generate_tts.py                  # Generate all scenes (1-6)
    python _Code/generate_tts.py --scenes 3 4 5 6 # Regenerate specific scenes
    python _Code/generate_tts.py --edge-tts       # Optional edge-tts fallback
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = PROJECT_ROOT / "media" / "audio"
CLONED_DIR = AUDIO_DIR / "cloned"
VOICE_SAMPLE = PROJECT_ROOT / "voice_sample.m4a"
VOICE_REF = PROJECT_ROOT / "voice_ref.wav"
VOICE_REF_CLIP = CLONED_DIR / "voice_ref_clip.wav"
NARRATION_SCRIPT = PROJECT_ROOT / "_Code" / "narration_script.txt"
DURATIONS_FILE = AUDIO_DIR / "durations.json"

# Exact transcript of the 8.8s clean speaker clip extracted from voice_ref.wav
REFERENCE_TRANSCRIPT = (
    "Hello, my name is Aradhya, and today we are exploring eigenvalues and eigenvectors in linear algebra."
)

# Exact rendered scene durations (seconds) from media/videos/scenes/1080p30/Scene*.mp4
SCENE_VIDEO_DURATIONS = {
    1: 34.000,
    2: 58.600,
    3: 54.333,
    4: 89.200,
    5: 50.467,
    6: 32.800,
}

# TTS phonetic cleanup overrides applied to spoken narration text so isolated
# math letters/IDs (e.g., "A minus", "M3", "e25b070764") are pronounced accurately.
TTS_REPLACEMENTS = [
    ("A minus lambda I", "matrix A, minus lambda I"),
    ("A minus three I", "matrix A, minus three I"),
    ("A minus two I", "matrix A, minus two I"),
    ("A times v-one", "Matrix A times v-one"),
    ("A times v-two", "Matrix A times v-two"),
    ("x plus y equals zero", "x, plus y, equals zero"),
    ("Now look at the vector minus one, one.", "Now, look at the vector: minus one, one."),
    ("Same direction, just stretched.", "Same direction, just stretched out."),
    ("e25b070764", "e two five b, zero seven zero seven six four"),
    ("M3 Internal Assessment", "M three Internal Assessment"),
]


def parse_narration_script(script_path: Path) -> dict[int, str]:
    """Parse _Code/narration_script.txt into {scene_num: text}."""
    text = script_path.read_text(encoding="utf-8")
    scenes: dict[int, str] = {}
    parts = re.split(r"SCENE\s+(\d+)\s*[—–-]", text)
    for i in range(1, len(parts) - 1, 2):
        scene_num = int(parts[i])
        content = parts[i + 1].strip()
        lines = content.split("\n")
        narration_lines = []
        past_header = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("---") or stripped.startswith("==="):
                past_header = True
                continue
            if past_header and stripped and not stripped.startswith("["):
                narration_lines.append(stripped)
        scenes[scene_num] = " ".join(narration_lines)
    return scenes


def normalize_text_for_tts(text: str) -> str:
    """Apply phonetic replacements for clean F5-TTS pronunciation."""
    for src, dst in TTS_REPLACEMENTS:
        text = text.replace(src, dst)
    return text


def get_audio_duration(filepath: str | Path) -> float:
    """Measure audio duration via ffprobe (with mutagen fallback)."""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(filepath)],
            text=True,
        ).strip()
        if out:
            return float(out)
    except Exception:
        pass
    from mutagen import File as MutagenFile
    mf = MutagenFile(str(filepath))
    if mf is not None and mf.info is not None:
        return float(mf.info.length)
    raise RuntimeError(f"Could not determine duration for {filepath}")


def ensure_voice_reference() -> Path:
    """Ensure voice_ref.wav and clean 8.8s voice_ref_clip.wav exist."""
    CLONED_DIR.mkdir(parents=True, exist_ok=True)
    if not VOICE_REF.exists():
        if not VOICE_SAMPLE.exists():
            raise FileNotFoundError(
                f"Neither {VOICE_REF} nor {VOICE_SAMPLE} found."
            )
        subprocess.run([
            "ffmpeg", "-y", "-i", str(VOICE_SAMPLE),
            "-ar", "22050", "-ac", "1",
            "-af", "afftdn=nf=-20,loudnorm=I=-16:TP=-1.5:LRA=11",
            str(VOICE_REF),
        ], capture_output=True, check=True)
    if not VOICE_REF_CLIP.exists():
        subprocess.run([
            "ffmpeg", "-y", "-i", str(VOICE_REF),
            "-t", "8.8", "-ar", "22050", "-ac", "1",
            str(VOICE_REF_CLIP),
        ], capture_output=True, check=True)
    return VOICE_REF_CLIP


def sync_and_normalize_scene(raw_wav: Path, target_dur: float, out_wav: Path, out_mp3: Path) -> float:
    """Trim excessive dead-air pauses, match exact video duration, and normalize loudness."""
    nosil_wav = raw_wav.with_suffix(".nosil.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_wav),
        "-af", "silenceremove=start_periods=1:stop_periods=-1:stop_duration=0.35:stop_threshold=-38dB",
        "-ar", "22050", "-ac", "1",
        str(nosil_wav),
    ], capture_output=True, check=True)

    trimmed_dur = get_audio_duration(nosil_wav)
    # Aim ~0.25s shorter than video boundary and pad trailing silence cleanly
    ratio = trimmed_dur / (target_dur - 0.25)
    if ratio < 0.85:
        # Don't stretch too slow; keep at least 0.90x and pad remainder
        tempo = max(0.90, ratio)
        af = f"atempo={tempo:.4f},apad=pad_dur={target_dur:.3f}"
    elif ratio <= 2.0:
        af = f"atempo={ratio:.4f},apad=pad_dur=0.5"
    else:
        half = ratio ** 0.5
        af = f"atempo={half:.4f},atempo={half:.4f},apad=pad_dur=0.5"

    # Export lossless 48kHz stereo loudness-normalized WAV for video merge
    subprocess.run([
        "ffmpeg", "-y", "-i", str(nosil_wav),
        "-af", f"{af},loudnorm=I=-16:TP=-1.5:LRA=11",
        "-t", f"{target_dur:.3f}",
        "-ar", "48000", "-ac", "2",
        str(out_wav),
    ], capture_output=True, check=True)

    # Also export MP3 mirror for standard compatibility
    subprocess.run([
        "ffmpeg", "-y", "-i", str(out_wav),
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(out_mp3),
    ], capture_output=True, check=True)

    nosil_wav.unlink(missing_ok=True)
    final_dur = get_audio_duration(out_wav)
    print(f"  Synced {raw_wav.name}: {trimmed_dur:.2f}s (atempo={ratio:.3f}) -> {final_dur:.2f}s (target {target_dur:.2f}s)")
    return final_dur


def generate_f5_tts(scenes_to_generate: list[int]) -> None:
    """Run local zero-shot F5-TTS voice cloning on specified scenes and sync all 1-6."""
    from f5_tts.api import F5TTS
    from f5_tts.infer.utils_infer import preprocess_ref_audio_text

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    ref_clip = ensure_voice_reference()
    parsed = parse_narration_script(NARRATION_SCRIPT)

    if scenes_to_generate:
        print(f"Loading F5-TTS (F5TTS_v1_Base) for scenes {scenes_to_generate}...")
        tts = F5TTS(model="F5TTS_v1_Base")
        ref_file, ref_text = preprocess_ref_audio_text(str(ref_clip), REFERENCE_TRANSCRIPT)
        for sn in scenes_to_generate:
            tts_text = normalize_text_for_tts(parsed[sn])
            raw_wav = CLONED_DIR / f"scene{sn}_raw.wav"
            print(f"\nSynthesizing Scene {sn} ({len(tts_text)} chars)...")
            tts.infer(
                ref_file=ref_file,
                ref_text=ref_text,
                gen_text=tts_text,
                file_wave=str(raw_wav),
                speed=1.08,
                seed=42,
            )
            print(f"  Raw generated duration: {get_audio_duration(raw_wav):.2f}s")

    print("\nSynchronizing timing & normalizing loudness across all Scenes 1-6...")
    durations = {}
    for sn in range(1, 7):
        raw_wav = CLONED_DIR / f"scene{sn}_raw.wav"
        if not raw_wav.exists():
            raise FileNotFoundError(f"Missing raw cloned WAV for scene {sn}: {raw_wav}")
        out_wav = CLONED_DIR / f"scene{sn}_sync.wav"
        out_mp3 = AUDIO_DIR / f"scene{sn}.mp3"
        durations[f"scene{sn}"] = sync_and_normalize_scene(
            raw_wav, SCENE_VIDEO_DURATIONS[sn], out_wav, out_mp3
        )

    DURATIONS_FILE.write_text(json.dumps(durations, indent=2), encoding="utf-8")
    print(f"\nSaved durations to {DURATIONS_FILE}")
    print(f"Total narration (Scenes 1-6): {sum(durations.values()):.2f}s")


async def generate_edge_tts_fallback() -> None:
    """Optional fallback generator using edge-tts (en-GB-RyanNeural)."""
    import edge_tts
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    parsed = parse_narration_script(NARRATION_SCRIPT)
    durations = {}
    for sn in range(1, 7):
        out_mp3 = AUDIO_DIR / f"scene{sn}.mp3"
        print(f"Generating scene{sn} via edge-tts...")
        communicate = edge_tts.Communicate(parsed[sn], "en-GB-RyanNeural", rate="+8%")
        await communicate.save(str(out_mp3))
        durations[f"scene{sn}"] = get_audio_duration(out_mp3)
    DURATIONS_FILE.write_text(json.dumps(durations, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate narration audio using F5-TTS voice cloning.")
    parser.add_argument("--scenes", type=int, nargs="*", default=[1, 2, 3, 4, 5, 6],
                        help="Scene numbers to synthesize (sync runs on all 1-6).")
    parser.add_argument("--sync-only", action="store_true",
                        help="Skip F5-TTS synthesis and only re-sync/normalize existing raw WAVs.")
    parser.add_argument("--edge-tts", action="store_true",
                        help="Use edge-tts fallback instead of local voice cloning.")
    args = parser.parse_args()

    if args.edge_tts:
        asyncio.run(generate_edge_tts_fallback())
    else:
        scenes = [] if args.sync_only else args.scenes
        generate_f5_tts(scenes)


if __name__ == "__main__":
    main()
