# Eigenvalues & Eigenvectors: Geometric Meaning and Calculation for a 2×2 Matrix

**M3 Internal Assessment – Animation Video**

| Field | Details |
|---|---|
| **Student** | ARADHYA |
| **Student ID** | e25b070764 |
| **Course** | Mathematics 3 (Linear Algebra and Calculus) |
| **Topic** | Eigenvalues and Eigenvectors |

---

## Learning Objective

By the end of this video, the viewer will be able to explain what eigenvalues and eigenvectors represent geometrically under a linear transformation, and calculate them step-by-step for a 2×2 matrix.

---

## Storyboard — 6-Scene Structure

| Scene | Purpose | Visuals | Narration Summary | Mathematics |
|---|---|---|---|---|
| **0. Opening** (~5s) | Title card | Title "Eigenvalues & Eigenvectors: Stretching Without Turning", student name, ID, course info on dark background | *No narration* | None |
| **1. Hook** (~30s) | Engage the viewer with a motivating question | A 2D grid transforms under a matrix; vectors rotate off their spans; pose the question about "invariant" directions | When a matrix transforms a grid, almost every vector changes direction. Are there special vectors that only stretch? Those are eigenvectors; their stretch factors are eigenvalues. | None |
| **2. Concepts** (~50s) | Define key terms and the eigen-equation | Show T(x) = Ax, then Av = λv with labelled braces for eigenvector and eigenvalue; cases for λ > 0, λ < 0, λ = 0; learning objective in a box | Define linear transformation, eigenvector, eigenvalue, and the equation Av = λv. Explain what different signs of λ mean geometrically. | Av = λv |
| **3. Visual Intuition** (~50s) | Show eigenvectors surviving a transformation | Grid + vectors under A = [[3,1],[0,2]]; general vectors rotate off dotted span lines; v₁ = [1,0] stretches 3×, v₂ = [-1,1] stretches 2× | Watch the grid transform. General vectors rotate, but v₁ and v₂ stay on their lines — only stretched by their eigenvalues. | A = [[3,1],[0,2]], v₁ = [1,0], v₂ = [-1,1] |
| **4. Worked Example** (~100s) | Step-by-step algebraic derivation | 4 steps: eigen-equation → characteristic equation det(A−λI) = 0 → solve for λ₁ = 3, λ₂ = 2 → null spaces for v₁, v₂ | Derive eigenvalues from det(A − λI) = 0, then find eigenvectors by solving each null space. | det(A−λI) = (3−λ)(2−λ) = 0; (A−3I)v = 0 → v₁ = [1,0]ᵀ; (A−2I)v = 0 → v₂ = [−1,1]ᵀ |
| **5. Verification** (~40s) | Confirm results numerically and visually; discuss negative/zero eigenvalues | Show Av₁ = 3v₁ and Av₂ = 2v₂ with checkmarks; bullet points for λ < 0 and λ = 0 interpretations | Verify both Av = λv checks. Explain what negative eigenvalues (flip) and zero eigenvalue (collapse) mean. | Av₁ = [3,0] = 3[1,0]; Av₂ = [−2,2] = 2[−1,1] |
| **6. Summary & Credits** (~30s) | Wrap up with takeaways, references, and AI disclosure | 3 takeaway bullet points; references list; AI disclosure statement | Three takeaways: eigenvectors are invariant directions; eigenvalues from det(A−λI) = 0; eigenvectors from null space. Credits and AI disclosure. | None |
