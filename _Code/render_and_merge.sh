#!/usr/bin/env bash
# render_and_merge.sh — Render all Manim scenes and combine with audio into final video
# Usage: ./render_and_merge.sh
set -euo pipefail

PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CODE_DIR="$PROJ_DIR/_Code"
MEDIA_DIR="$PROJ_DIR/media"
AUDIO_DIR="$MEDIA_DIR/audio"
VIDEO_DIR="$MEDIA_DIR/videos"
SCENE_FILE="$CODE_DIR/scenes.py"
OUTPUT="$PROJ_DIR/_Video.mp4"

# Activate virtual environment
source "$PROJ_DIR/venv/bin/activate"

echo "=== Step 0: Verify mathematics ==="
python3 "$CODE_DIR/verify_eigen.py"

echo ""
echo "=== Step 1: Generate TTS audio ==="
python3 "$CODE_DIR/generate_tts.py"

echo ""
echo "=== Step 2: Render each scene with Manim ==="
SCENES=("Scene0_Opening" "Scene1_Hook" "Scene2_Concepts" "Scene3_VisualIntuition" "Scene4_WorkedExample" "Scene5_Verification" "Scene6_Summary")

for scene in "${SCENES[@]}"; do
    echo "  Rendering $scene..."
    manim render -qh --fps 30 --format mp4 "$SCENE_FILE" "$scene"
done

echo ""
echo "=== Step 3: Combine scenes with audio using FFmpeg ==="

# Find rendered video files
VDIR="$MEDIA_DIR/videos/scenes/1080p30"
mkdir -p "$MEDIA_DIR/temp"

# Scene 0 has no audio — just use video
SCENE0_VID=$(ls "$VDIR"/Scene0_Opening.mp4 2>/dev/null || echo "")
if [ -z "$SCENE0_VID" ]; then
    echo "ERROR: Scene0 video not found in $VDIR"
    exit 1
fi

# For each scene with audio, merge video + audio
CONCAT_LIST="$MEDIA_DIR/temp/concat.txt"
> "$CONCAT_LIST"

# Scene 0: video only (title card) - add silent 48kHz stereo audio track
ffmpeg -y -i "$SCENE0_VID" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -c:v copy -c:a aac -ar 48000 -ac 2 -b:a 192k -shortest "$MEDIA_DIR/temp/scene0_final.mp4" 2>/dev/null
echo "file 'scene0_final.mp4'" >> "$CONCAT_LIST"

# Scenes 1-6: merge video with audio (normalized to 48kHz stereo AAC)
for i in 1 2 3 4 5 6; do
    scene="${SCENES[$i]}"
    vid_file="$VDIR/${scene}.mp4"
    audio_file="$AUDIO_DIR/scene${i}.mp3"

    if [ ! -f "$vid_file" ]; then
        echo "ERROR: $vid_file not found"
        exit 1
    fi
    if [ ! -f "$audio_file" ]; then
        echo "ERROR: $audio_file not found"
        exit 1
    fi

    # Get video and audio durations
    vid_dur=$(ffprobe -v quiet -print_format json -show_format "$vid_file" | python3 -c "import sys,json; print(json.load(sys.stdin)['format']['duration'])")
    aud_dur=$(ffprobe -v quiet -print_format json -show_format "$audio_file" | python3 -c "import sys,json; print(json.load(sys.stdin)['format']['duration'])")
    echo "  Scene $i: video=${vid_dur}s audio=${aud_dur}s"

    # Merge: use the audio duration / shortest with clean 48kHz stereo AAC
    ffmpeg -y -i "$vid_file" -i "$audio_file" \
        -c:v copy -c:a aac -ar 48000 -ac 2 -b:a 192k \
        -shortest \
        "$MEDIA_DIR/temp/scene${i}_final.mp4" 2>/dev/null

    echo "file 'scene${i}_final.mp4'" >> "$CONCAT_LIST"
done

echo ""
echo "=== Step 4: Concatenate all scenes ==="
cd "$MEDIA_DIR/temp"
ffmpeg -y -f concat -safe 0 -i concat.txt -c:v copy -c:a copy -movflags +faststart "$OUTPUT" 2>/dev/null

# Check file size; if over 100MB, re-encode with CRF 24
FILESIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo "0")
if [ "$FILESIZE" -gt 104857600 ]; then
    echo "File size ($(( FILESIZE / 1048576 )) MB) exceeds 100 MB. Re-encoding with CRF 24..."
    ffmpeg -y -i "$OUTPUT" -c:v libx264 -crf 24 -preset slow -c:a copy -movflags +faststart "$MEDIA_DIR/temp/_Video_compressed.mp4"
    mv "$MEDIA_DIR/temp/_Video_compressed.mp4" "$OUTPUT"
fi

echo ""
echo "=== Step 5: Quality check ==="
ffprobe -v quiet -print_format json -show_format -show_streams "$OUTPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
fmt = data['format']
dur = float(fmt['duration'])
print(f'Duration: {dur:.1f}s ({dur/60:.1f} min)')
print(f'Size: {int(fmt[\"size\"])/1048576:.1f} MB')
for s in data['streams']:
    if s['codec_type'] == 'video':
        print(f'Video: {s[\"codec_name\"]} {s[\"width\"]}x{s[\"height\"]} {s.get(\"r_frame_rate\",\"?\")} fps')
    elif s['codec_type'] == 'audio':
        print(f'Audio: {s[\"codec_name\"]} {s.get(\"sample_rate\",\"?\")} Hz')
if dur > 420:
    print('WARNING: Duration exceeds 7:00')
elif dur > 330:
    print('Duration OK (under 7:00)')
else:
    print('Duration OK')
"

echo ""
echo "=== Done! Output: $OUTPUT ==="
