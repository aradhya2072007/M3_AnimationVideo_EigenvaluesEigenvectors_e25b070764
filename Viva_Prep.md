# Viva Preparation — 15 Likely Questions with Short Answers

**Eigenvalues & Eigenvectors — M3 Internal Assessment**
**Student:** ARADHYA | **Student ID:** e25b070764

---

## Mathematics Questions

### Q1. What is an eigenvector?
An eigenvector **v** of a matrix A is a non-zero vector whose direction is unchanged by the transformation A. Mathematically, Av = λv for some scalar λ.

### Q2. What is an eigenvalue?
The eigenvalue λ is the scalar factor by which the eigenvector is stretched (or compressed/flipped) when the matrix A acts on it.

### Q3. Why must an eigenvector be non-zero?
If v = 0, then Av = λv = 0 is trivially true for every λ, so the equation gives us no useful information. We need non-zero v to identify meaningful invariant directions.

### Q4. How do you find eigenvalues?
Set up the characteristic equation det(A − λI) = 0 and solve for λ. For a 2×2 matrix, this gives a quadratic in λ.

### Q5. Walk through the characteristic equation for A = [[3,1],[0,2]].
A − λI = [[3−λ, 1], [0, 2−λ]]. The determinant is (3−λ)(2−λ) − (1)(0) = (3−λ)(2−λ) = 0. So λ₁ = 3 and λ₂ = 2.

### Q6. How do you find eigenvectors once you have the eigenvalues?
For each eigenvalue λ, solve the homogeneous system (A − λI)v = 0 to find the null space. Any non-zero vector in that null space is an eigenvector.

### Q7. For λ₁ = 3, show the null-space calculation.
A − 3I = [[0,1],[0,−1]]. The system says y = 0, x is free. So v₁ = t[1,0] for any t ≠ 0. We pick v₁ = [1,0].

### Q8. What does a negative eigenvalue mean geometrically?
The eigenvector's direction is reversed (flipped through the origin) in addition to being scaled by |λ|.

### Q9. What does an eigenvalue of zero mean?
The eigenvector is collapsed to the origin — that direction lies in the null space of A. The transformation destroys information along that direction.

### Q10. Can a 2×2 matrix have complex eigenvalues? What does that mean?
Yes. Complex eigenvalues (occurring in conjugate pairs for real matrices) indicate a rotation — no real eigenvector direction is preserved. Example: a pure rotation matrix.

---

## Visual & Code Questions

### Q11. Why did you choose these specific colours?
Green for î (basis vector i-hat) and red for ĵ (basis vector j-hat) follow the 3Blue1Brown convention. Yellow for v₁ and cyan for v₂ provide high-contrast, distinguishable colours against the dark background. Grey for general vectors keeps them visually subordinate.

### Q12. How do you keep the audio and animation in sync?
Each rendered Manim scene (`Scene0` through `Scene6`) has an exact known duration recorded in `durations.json`. After F5-TTS generates each scene's cloned narration WAV, FFmpeg measures its length with `ffprobe`, tightens excess pauses (`silenceremove`), and applies gentle `atempo` time-stretching (or trailing silence padding with `apad`) so every voice track matches its scene video duration cleanly with zero drift across scene transitions.

### Q13. What tool generates the narration, and which voice is used?
The narration is cloned from the student's own 43-second voice recording (`voice_sample.m4a`, pre-processed with FFmpeg `afftdn` noise reduction and `loudnorm` into `voice_ref.wav`) using the local zero-shot **F5-TTS** (`F5TTS_v1_Base`) model running on Apple Silicon MPS, with FFmpeg `loudnorm` (`-16 LUFS`) applied before merging into `_Video.mp4`. (`edge-tts` is retained only as an optional fallback.)

### Q14. How is the final video assembled?
FFmpeg merges each scene's rendered video with its audio track, then concatenates all scenes using the concat demuxer. The output is H.264 video + AAC audio at 1920×1080, 30fps.

### Q15. What does `apply_matrix` do in Manim?
`apply_matrix(M)` applies the linear transformation defined by the 2×2 matrix M to a Mobject. For a NumberPlane, it warps the entire grid. For an Arrow, it moves its tip according to the matrix multiplication. This is used in Scene 3 to show the transformation visually.
