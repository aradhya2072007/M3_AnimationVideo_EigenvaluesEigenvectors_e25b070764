# Eigenvalues & Eigenvectors: Geometric Meaning and Calculation for a 2×2 Matrix

**M3 Internal Assessment – Animation Video**

| | |
|---|---|
| **Student** | ARADHYA |
| **Student ID** | e25b070764 |
| **Course** | Mathematics 3 (Linear Algebra and Calculus) |

---

## Learning Objective

> By the end of this video, the viewer will be able to explain what eigenvalues and eigenvectors represent geometrically under a linear transformation, and calculate them step-by-step for a 2×2 matrix.

---

## Repository Contents

| File / Folder | Description |
|---|---|
| `_Video.mp4` | Final narrated animation video (1920×1080, H.264 + AAC, ~5 min) |
| `_Code/` | All source code |
| `_Code/scenes.py` | Manim scene classes (7 scenes) |
| `_Code/generate_tts.py` | Voice-cloned narration generator (F5-TTS zero-shot voice cloning, with edge-tts fallback) |
| `_Code/verify_eigen.py` | NumPy verification of eigenvalue calculations |
| `_Code/render_and_merge.sh` | Build pipeline: verify → TTS → render → merge |
| `_Code/narration_script.txt` | Full narration text by scene |
| `_Code/requirements.txt` | Python dependencies |
| `voice_sample.m4a` | Student's original 43-second voice recording (Apple Voice Memos) |
| `voice_ref.wav` | Pre-processed 22.05 kHz mono speaker reference (`afftdn` + `loudnorm`) |
| `Storyboard.pdf` | 6-scene storyboard with learning objective |
| `Narration_Script.pdf` | Complete narration script |
| `Code_Walkthrough.pdf` | Plain-English explanation of every code file |
| `Viva_Prep.pdf` | 15 viva questions with answers |
| `README.md` | This file |

---

## Tools Used

| Tool | Purpose |
|---|---|
| **Manim Community Edition** (Python) | All mathematical animations and scene rendering |
| **LaTeX** (via MathTex in Manim) | Typesetting mathematical equations |
| **F5-TTS** (`F5TTS_v1_Base`) | Local zero-shot voice cloning from the student's voice sample (`voice_ref.wav`) |
| **FFmpeg** | Noise reduction (`afftdn`), loudness normalization (`loudnorm`), timing sync, and A/V merge |
| **NumPy** | Eigenvalue/eigenvector verification |

---

## How to Re-Render

```bash
# 1. Clone this repository
git clone https://github.com/aradhya2072007/M3_AnimationVideo_EigenvaluesEigenvectors_e25b070764.git
cd M3_AnimationVideo_EigenvaluesEigenvectors_e25b070764

# 2. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r _Code/requirements.txt

# 3. Ensure system dependencies are installed
# macOS: brew install cairo pango ffmpeg texlive
# Ubuntu: sudo apt install libcairo2-dev libpango1.0-dev ffmpeg texlive-full

# 4. Run the full pipeline
chmod +x _Code/render_and_merge.sh
bash _Code/render_and_merge.sh
```

---

## References

1. Gilbert Strang, *Introduction to Linear Algebra*, 5th Edition, Wellesley-Cambridge Press.
2. David C. Lay, *Linear Algebra and Its Applications*, 6th Edition, Pearson.
3. 3Blue1Brown, *Essence of Linear Algebra* (YouTube series), [https://www.3blue1brown.com/topics/linear-algebra](https://www.3blue1brown.com/topics/linear-algebra)
4. Manim Community Documentation, [https://docs.manim.community/](https://docs.manim.community/)

---

## AI Disclosure

Script, animation code and narration text were produced with the help of Claude (Anthropic) and Gemini inside Antigravity. Voice: Cloned from the student's own voice recording (`voice_sample.m4a` → `voice_ref.wav`) using the local zero-shot F5-TTS (`F5TTS_v1_Base`) model. All mathematics was checked by the student.
