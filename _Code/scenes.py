#!/usr/bin/env python3
"""
Eigenvalues & Eigenvectors — Manim Animation Scenes
Student: ARADHYA | ID: e25b070764 | M3 Internal Assessment
"""
from manim import *
import numpy as np
import json
import os

# ── Colour palette ──────────────────────────────────────────────────
IHAT_COLOR   = GREEN        # basis vector i-hat
JHAT_COLOR   = RED          # basis vector j-hat
V1_COLOR     = YELLOW       # eigenvector v1
V2_COLOR     = "#00FFFF"    # eigenvector v2 (pure cyan)
GEN_COLOR    = GREY_B       # general transformed vectors
BG_COLOR     = "#1a1a2e"    # dark background

# ── Matrix and eigen-data ───────────────────────────────────────────
A = np.array([[3, 1], [0, 2]])
LAMBDA1, LAMBDA2 = 3, 2
V1 = np.array([1, 0])
V2 = np.array([-1, 1])

# ── Load durations ──────────────────────────────────────────────────
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media", "audio")
DUR_PATH = os.path.join(AUDIO_DIR, "durations.json")
if os.path.exists(DUR_PATH):
    with open(DUR_PATH) as f:
        DURATIONS = json.load(f)
else:
    # Fallback defaults if audio not generated yet
    DURATIONS = {
        "scene1": 30, "scene2": 50, "scene3": 50,
        "scene4": 100, "scene5": 40, "scene6": 30,
    }


# ════════════════════════════════════════════════════════════════════
# SCENE 0 — Opening Title Card (~5 s)
# ════════════════════════════════════════════════════════════════════
class Scene0_Opening(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "Eigenvalues & Eigenvectors",
            font_size=56, color=WHITE, weight=BOLD,
        ).shift(UP * 1.8)
        subtitle = Text(
            "Stretching Without Turning",
            font_size=36, color=BLUE_C,
        ).next_to(title, DOWN, buff=0.4)
        line = Line(LEFT * 4.5, RIGHT * 4.5, color=BLUE_C, stroke_width=2).next_to(subtitle, DOWN, buff=0.4)
        course = Text(
            "M3 Internal Assessment – Animation Video",
            font_size=28, color=GREY_B,
        ).next_to(line, DOWN, buff=0.5)
        name = Text("ARADHYA", font_size=36, color=WHITE, weight=BOLD).next_to(course, DOWN, buff=0.4)
        sid = Text("Student ID: e25b070764", font_size=28, color=GREY_B).next_to(name, DOWN, buff=0.2)

        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            FadeIn(subtitle, shift=DOWN * 0.3),
            run_time=1.0,
        )
        self.play(
            Create(line),
            FadeIn(course, shift=UP * 0.2),
            FadeIn(name, shift=UP * 0.2),
            FadeIn(sid, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(3.0)


# ════════════════════════════════════════════════════════════════════
# SCENE 1 — Hook (~30 s)
# ════════════════════════════════════════════════════════════════════
class Scene1_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene1", 30)

        # Create a number plane / grid
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=10, y_length=7,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.4},
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.3)

        # Basis vectors i-hat (green) and j-hat (red)
        ihat = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color=IHAT_COLOR, stroke_width=4)
        jhat = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0, color=JHAT_COLOR, stroke_width=4)
        ihat_lbl = Text("i-hat", font_size=20, color=IHAT_COLOR).next_to(ihat.get_end(), DOWN, buff=0.12)
        jhat_lbl = Text("j-hat", font_size=20, color=JHAT_COLOR).next_to(jhat.get_end(), LEFT, buff=0.12)

        # A few sample general vectors
        vectors = VGroup()
        vec_dirs = [(1, 1), (2, 0.8), (1.2, 1.8), (-1.2, 0.6), (1.8, -0.8), (-1.5, -1)]
        for vx, vy in vec_dirs:
            v = Arrow(
                plane.c2p(0, 0), plane.c2p(vx, vy),
                buff=0, color=GEN_COLOR, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.15,
            )
            vectors.add(v)

        title = Text("When a matrix transforms a grid...", font_size=36, color=WHITE).to_edge(UP, buff=0.4)

        self.play(FadeIn(plane), Write(title), run_time=1.5)
        self.play(
            GrowArrow(ihat), GrowArrow(jhat), FadeIn(ihat_lbl), FadeIn(jhat_lbl),
            LaggedStartMap(GrowArrow, vectors, lag_ratio=0.15),
            run_time=2.0
        )

        # Apply the transformation matrix
        matrix = [[3, 1], [0, 2]]
        question = Text(
            "Are there special vectors that only stretch,\nnever rotate?",
            font_size=32, color=YELLOW,
            line_spacing=1.3,
        ).to_edge(UP, buff=0.5)

        self.play(
            plane.animate.apply_matrix(matrix),
            ihat.animate.apply_matrix(matrix),
            jhat.animate.apply_matrix(matrix),
            *[v.animate.apply_matrix(matrix) for v in vectors],
            FadeTransform(title, question),
            FadeOut(ihat_lbl), FadeOut(jhat_lbl),
            run_time=3.5,
        )

        # Highlight the concept
        eigenvec_label = Text("Eigenvectors!", font_size=48, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.8)
        eigenval_label = Text("Eigenvalues = stretch factors", font_size=30, color=V2_COLOR).next_to(eigenvec_label, DOWN, buff=0.3)

        self.wait(1.5)
        self.play(FadeIn(eigenvec_label, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(eigenval_label, shift=UP * 0.2), run_time=0.8)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)


# ════════════════════════════════════════════════════════════════════
# SCENE 2 — Concept Introduction (~50 s)
# ════════════════════════════════════════════════════════════════════
class Scene2_Concepts(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene2", 50)

        # Title
        title = Text("Linear Transformation & Eigenvectors", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        # T(x) = Ax
        eq1 = MathTex(r"T(\mathbf{x}) = A\mathbf{x}", font_size=48, color=WHITE).shift(UP * 1.5)
        desc1 = Text("A linear transformation maps every vector x to Ax", font_size=26, color=GREY_B).next_to(eq1, DOWN, buff=0.3)
        self.play(Write(eq1), FadeIn(desc1), run_time=2.0)
        self.wait(2.0)

        # Eigen equation
        eq2 = MathTex(r"A\mathbf{v} = \lambda \mathbf{v}", font_size=56, color=YELLOW).shift(UP * 0.1)
        
        # Side callout boxes to prevent overlap
        ev_box = VGroup(
            Text("Eigenvector v (non-zero):", font_size=22, color=V1_COLOR, weight=BOLD),
            Text("Direction is unchanged", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).shift(LEFT * 3.5 + DOWN * 1.0)

        el_box = VGroup(
            Text("Eigenvalue λ (scalar):", font_size=22, color=V2_COLOR, weight=BOLD),
            Text("Stretch / scale factor", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).shift(RIGHT * 3.5 + DOWN * 1.0)

        arrow_v = Arrow(ev_box.get_top(), eq2.get_bottom() + LEFT * 0.2, color=V1_COLOR, stroke_width=2.5, buff=0.15)
        arrow_l = Arrow(el_box.get_top(), eq2.get_bottom() + RIGHT * 0.35, color=V2_COLOR, stroke_width=2.5, buff=0.15)

        self.play(FadeOut(desc1), run_time=0.5)
        self.play(Write(eq2), run_time=2.0)
        self.wait(1.5)
        self.play(
            FadeIn(ev_box, shift=UP * 0.2), GrowArrow(arrow_v),
            FadeIn(el_box, shift=UP * 0.2), GrowArrow(arrow_l),
            run_time=1.5,
        )
        self.wait(3.0)

        # Lambda cases
        cases = VGroup(
            MathTex(r"\lambda > 0", r"\text{: stretches along its line}", font_size=28, color=GREEN_B),
            MathTex(r"\lambda < 0", r"\text{: flips direction \& stretches}", font_size=28, color=RED_B),
            MathTex(r"\lambda = 0", r"\text{: collapses to origin (null space)}", font_size=28, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 2.2)

        self.play(
            FadeOut(ev_box), FadeOut(arrow_v),
            FadeOut(el_box), FadeOut(arrow_l),
            run_time=0.5,
        )
        for c in cases:
            self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.5)

        self.wait(2.0)

        # Clear and show learning objective
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        lo_title = Text("Learning Objective", font_size=40, color=BLUE_C, weight=BOLD).to_edge(UP, buff=0.8)
        lo_text = Text(
            "By the end of this video, the viewer will be able to\n"
            "explain what eigenvalues and eigenvectors represent\n"
            "geometrically under a linear transformation, and\n"
            "calculate them step-by-step for a 2×2 matrix.",
            font_size=28, color=WHITE, line_spacing=1.4,
        ).next_to(lo_title, DOWN, buff=0.6)

        box = SurroundingRectangle(lo_text, color=BLUE_C, buff=0.3, corner_radius=0.1)

        self.play(Write(lo_title), run_time=0.8)
        self.play(FadeIn(lo_text), Create(box), run_time=1.5)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)


# ════════════════════════════════════════════════════════════════════
# SCENE 3 — Visual Intuition (~50 s)
# ════════════════════════════════════════════════════════════════════
class Scene3_VisualIntuition(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene3", 50)

        # Create plane
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 4, 1],
            x_length=12, y_length=8,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_color": GREY, "stroke_width": 1.5},
        )

        matrix_label = MathTex(
            r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}",
            font_size=36, color=WHITE,
        ).to_corner(UR, buff=0.5)
        bg_rect = BackgroundRectangle(matrix_label, color=BG_COLOR, fill_opacity=0.85, buff=0.15)

        # Basis vectors (before transformation)
        ihat = Arrow(plane.c2p(0,0), plane.c2p(1,0), buff=0, color=IHAT_COLOR, stroke_width=4)
        jhat = Arrow(plane.c2p(0,0), plane.c2p(0,1), buff=0, color=JHAT_COLOR, stroke_width=4)
        ihat_label = MathTex(r"\hat{\imath}", font_size=28, color=IHAT_COLOR).next_to(ihat.get_end(), DOWN, buff=0.15)
        jhat_label = MathTex(r"\hat{\jmath}", font_size=28, color=JHAT_COLOR).next_to(jhat.get_end(), LEFT, buff=0.15)

        # Eigenvectors (before transformation)
        ev1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), buff=0, color=V1_COLOR, stroke_width=4)
        ev2 = Arrow(plane.c2p(0,0), plane.c2p(-1,1), buff=0, color=V2_COLOR, stroke_width=4)
        ev1_label = MathTex(r"\mathbf{v}_1 = \begin{bmatrix}1\\0\end{bmatrix}", font_size=26, color=V1_COLOR)
        ev2_label = MathTex(r"\mathbf{v}_2 = \begin{bmatrix}-1\\1\end{bmatrix}", font_size=26, color=V2_COLOR)

        # Span lines (dotted) for eigenvectors
        span1 = DashedLine(plane.c2p(-5, 0), plane.c2p(5, 0), color=V1_COLOR, stroke_width=1.5, dash_length=0.1)
        span2 = DashedLine(plane.c2p(4, -4), plane.c2p(-4, 4), color=V2_COLOR, stroke_width=1.5, dash_length=0.1)

        # Some general vectors (not eigenvectors)
        gen_vecs = VGroup()
        gen_spans = VGroup()
        gen_dirs = [(1, 1.5), (2, 1), (-1.5, -0.5), (0.5, 2)]
        for gx, gy in gen_dirs:
            gv = Arrow(plane.c2p(0,0), plane.c2p(gx, gy), buff=0, color=GEN_COLOR, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.12)
            norm = np.sqrt(gx**2 + gy**2)
            gspan = DashedLine(
                plane.c2p(-4*gx/norm, -4*gy/norm),
                plane.c2p(4*gx/norm, 4*gy/norm),
                color=GREY, stroke_width=1, dash_length=0.08, stroke_opacity=0.5,
            )
            gen_vecs.add(gv)
            gen_spans.add(gspan)

        self.play(FadeIn(plane), run_time=1.0)
        self.play(FadeIn(bg_rect), Write(matrix_label), run_time=1.0)

        # Show eigenvectors and basis vector j-hat with span lines
        self.play(
            GrowArrow(ev1), GrowArrow(ev2), GrowArrow(jhat),
            Create(span1), Create(span2),
            run_time=1.5,
        )
        ev1_label.next_to(ev1.get_end(), UP + RIGHT, buff=0.15)
        ev2_label.next_to(ev2.get_end(), UP + LEFT, buff=0.15)
        jhat_label.next_to(jhat.get_end(), LEFT, buff=0.15)
        self.play(FadeIn(ev1_label), FadeIn(ev2_label), FadeIn(jhat_label), run_time=0.8)

        # Show general vectors
        self.play(
            LaggedStartMap(GrowArrow, gen_vecs, lag_ratio=0.1),
            LaggedStartMap(Create, gen_spans, lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(2.0)

        # Apply the transformation
        title = Text("Applying transformation A", font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        bg_title = BackgroundRectangle(title, color=BG_COLOR, fill_opacity=0.85, buff=0.1)
        self.play(FadeIn(bg_title), Write(title), run_time=0.8)

        matrix = [[3, 1], [0, 2]]
        self.play(
            plane.animate.apply_matrix(matrix),
            ev1.animate.apply_matrix(matrix),
            ev2.animate.apply_matrix(matrix),
            jhat.animate.apply_matrix(matrix),
            *[gv.animate.apply_matrix(matrix) for gv in gen_vecs],
            FadeOut(ev1_label), FadeOut(ev2_label), FadeOut(jhat_label),
            run_time=4.0,
        )

        # Show labels after transformation
        note_gen = Text("General vectors & j-hat rotated\noff their span lines!", font_size=24, color=RED_B).to_edge(LEFT, buff=0.5).shift(DOWN)
        bg_note_gen = BackgroundRectangle(note_gen, color=BG_COLOR, fill_opacity=0.85, buff=0.1)

        # Eigenvector result labels
        ev1_result = MathTex(
            r"\mathbf{v}_1 \to 3\mathbf{v}_1", font_size=30, color=V1_COLOR,
        ).to_corner(DL, buff=0.5).shift(UP * 0.5)
        ev2_result = MathTex(
            r"\mathbf{v}_2 \to 2\mathbf{v}_2", font_size=30, color=V2_COLOR,
        ).next_to(ev1_result, UP, buff=0.3)
        bg_ev = BackgroundRectangle(VGroup(ev1_result, ev2_result), color=BG_COLOR, fill_opacity=0.85, buff=0.15)

        self.play(FadeIn(bg_note_gen), FadeIn(note_gen), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(bg_ev), Write(ev1_result), Write(ev2_result), run_time=1.5)

        note_eigen = Text("Eigenvectors stayed on\ntheir lines — only stretched!", font_size=24, color=GREEN_B).to_edge(RIGHT, buff=0.5).shift(DOWN)
        bg_note_e = BackgroundRectangle(note_eigen, color=BG_COLOR, fill_opacity=0.85, buff=0.1)
        self.play(FadeIn(bg_note_e), FadeIn(note_eigen), run_time=1.0)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)


# ════════════════════════════════════════════════════════════════════
# SCENE 4 — Worked Example (~100 s)
# ════════════════════════════════════════════════════════════════════
class Scene4_WorkedExample(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene4", 100)

        title = Text("Step-by-Step Calculation", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.0)

        # Step 1: eigen equation
        step1_title = Text("Step 1: Eigen equation", font_size=28, color=BLUE_C).to_edge(LEFT, buff=1).shift(UP * 2)
        eq1a = MathTex(r"A\mathbf{v} = \lambda \mathbf{v}", font_size=42).next_to(step1_title, DOWN, buff=0.3, aligned_edge=LEFT)
        eq1b = MathTex(r"(A - \lambda I)\mathbf{v} = \mathbf{0}", font_size=42).next_to(eq1a, DOWN, buff=0.3, aligned_edge=LEFT)
        eq1c = MathTex(r"\det(A - \lambda I) = 0", font_size=42, color=YELLOW).next_to(eq1b, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(step1_title), run_time=0.8)
        self.play(Write(eq1a), run_time=1.5)
        self.wait(1.5)
        self.play(Write(eq1b), run_time=1.5)
        self.wait(1.0)
        self.play(Write(eq1c), run_time=1.5)
        self.wait(2.0)

        # Clear for Step 2
        self.play(*[FadeOut(m) for m in [step1_title, eq1a, eq1b, eq1c]], run_time=0.8)

        # Step 2: Characteristic equation
        step2_title = Text("Step 2: Characteristic equation", font_size=28, color=BLUE_C).to_edge(LEFT, buff=0.8).shift(UP * 2.3)

        mat_A = MathTex(
            r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}",
            font_size=38,
        ).next_to(step2_title, DOWN, buff=0.3, aligned_edge=LEFT)

        eq2a = MathTex(
            r"A - \lambda I = \begin{bmatrix} 3-\lambda & 1 \\ 0 & 2-\lambda \end{bmatrix}",
            font_size=38,
        ).next_to(mat_A, DOWN, buff=0.4, aligned_edge=LEFT)

        eq2b = MathTex(
            r"\det(A - \lambda I) = (3-\lambda)(2-\lambda) - (1)(0)",
            font_size=36,
        ).next_to(eq2a, DOWN, buff=0.4, aligned_edge=LEFT)

        eq2c = MathTex(
            r"= (3-\lambda)(2-\lambda) = 0",
            font_size=36, color=YELLOW,
        ).next_to(eq2b, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 0.5)

        self.play(Write(step2_title), run_time=0.8)
        self.play(Write(mat_A), run_time=1.5)
        self.wait(1.0)
        self.play(Write(eq2a), run_time=2.0)
        self.wait(1.5)
        self.play(Write(eq2b), run_time=2.0)
        self.wait(1.0)
        self.play(Write(eq2c), run_time=1.5)
        self.wait(1.5)

        # Eigenvalues result
        result_ev = MathTex(
            r"\lambda_1 = 3, \quad \lambda_2 = 2",
            font_size=44, color=GREEN_B,
        ).next_to(eq2c, DOWN, buff=0.5)
        box_ev = SurroundingRectangle(result_ev, color=GREEN_B, buff=0.15, corner_radius=0.08)

        self.play(Write(result_ev), Create(box_ev), run_time=1.5)
        self.wait(2.0)

        # Clear for Step 3
        self.play(*[FadeOut(m) for m in [step2_title, mat_A, eq2a, eq2b, eq2c, result_ev, box_ev]], run_time=0.8)

        # Step 3: Find v1 for lambda1 = 3
        step3_title = Text("Step 3: Eigenvector for λ₁ = 3", font_size=28, color=BLUE_C).to_edge(LEFT, buff=0.8).shift(UP * 2.5)

        eq3a = MathTex(
            r"(A - 3I)\mathbf{v} = \mathbf{0}",
            font_size=38,
        ).next_to(step3_title, DOWN, buff=0.3, aligned_edge=LEFT)

        eq3b = MathTex(
            r"\begin{bmatrix} 0 & 1 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}",
            font_size=36,
        ).next_to(eq3a, DOWN, buff=0.3, aligned_edge=LEFT)

        eq3c = MathTex(r"y = 0, \quad x \text{ is free}", font_size=34).next_to(eq3b, DOWN, buff=0.3, aligned_edge=LEFT)

        v1_result = MathTex(
            r"\mathbf{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=42, color=V1_COLOR,
        ).next_to(eq3c, DOWN, buff=0.4)
        box_v1 = SurroundingRectangle(v1_result, color=V1_COLOR, buff=0.15, corner_radius=0.08)

        self.play(Write(step3_title), run_time=0.8)
        self.play(Write(eq3a), run_time=1.5)
        self.wait(1.0)
        self.play(Write(eq3b), run_time=2.0)
        self.wait(1.0)
        self.play(Write(eq3c), run_time=1.5)
        self.wait(1.0)
        self.play(Write(v1_result), Create(box_v1), run_time=1.5)
        self.wait(2.0)

        # Clear for Step 4
        self.play(*[FadeOut(m) for m in [step3_title, eq3a, eq3b, eq3c, v1_result, box_v1]], run_time=0.8)

        # Step 4: Find v2 for lambda2 = 2
        step4_title = Text("Step 4: Eigenvector for λ₂ = 2", font_size=28, color=BLUE_C).to_edge(LEFT, buff=0.8).shift(UP * 2.5)

        eq4a = MathTex(
            r"(A - 2I)\mathbf{v} = \mathbf{0}",
            font_size=38,
        ).next_to(step4_title, DOWN, buff=0.3, aligned_edge=LEFT)

        eq4b = MathTex(
            r"\begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}",
            font_size=36,
        ).next_to(eq4a, DOWN, buff=0.3, aligned_edge=LEFT)

        eq4c = MathTex(r"x + y = 0 \implies y = -x", font_size=34).next_to(eq4b, DOWN, buff=0.3, aligned_edge=LEFT)

        v2_result = MathTex(
            r"\mathbf{v}_2 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}",
            font_size=42, color=V2_COLOR,
        ).next_to(eq4c, DOWN, buff=0.4)
        box_v2 = SurroundingRectangle(v2_result, color=V2_COLOR, buff=0.15, corner_radius=0.08)

        self.play(Write(step4_title), run_time=0.8)
        self.play(Write(eq4a), run_time=1.5)
        self.wait(1.0)
        self.play(Write(eq4b), run_time=2.0)
        self.wait(1.0)
        self.play(Write(eq4c), run_time=1.5)
        self.wait(1.0)
        self.play(Write(v2_result), Create(box_v2), run_time=1.5)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)


# ════════════════════════════════════════════════════════════════════
# SCENE 5 — Interpretation & Verification (~40 s)
# ════════════════════════════════════════════════════════════════════
class Scene5_Verification(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene5", 40)

        title = Text("Verification", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Verify v1 (left column)
        ver1_title = Text("Check v₁ (λ₁ = 3):", font_size=26, color=V1_COLOR, weight=BOLD).shift(UP * 1.8 + LEFT * 3.5)
        ver1a = MathTex(
            r"A\mathbf{v}_1 = \begin{bmatrix}3&1\\0&2\end{bmatrix}\begin{bmatrix}1\\0\end{bmatrix} = \begin{bmatrix}3\\0\end{bmatrix}",
            font_size=30,
        ).next_to(ver1_title, DOWN, buff=0.35, aligned_edge=LEFT)
        ver1b = MathTex(
            r"3\mathbf{v}_1 = 3\begin{bmatrix}1\\0\end{bmatrix} = \begin{bmatrix}3\\0\end{bmatrix}",
            font_size=30,
        ).next_to(ver1a, DOWN, buff=0.35, aligned_edge=LEFT)
        check1 = MathTex(r"\checkmark \text{ Matches!}", font_size=32, color=GREEN).next_to(ver1b, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(ver1_title), run_time=0.5)
        self.play(Write(ver1a), run_time=1.5)
        self.wait(0.5)
        self.play(Write(ver1b), run_time=1.5)
        self.play(FadeIn(check1, scale=1.3), run_time=0.5)
        self.wait(1.0)

        # Verify v2 (right column)
        ver2_title = Text("Check v₂ (λ₂ = 2):", font_size=26, color=V2_COLOR, weight=BOLD).shift(UP * 1.8 + RIGHT * 0.8)
        ver2a = MathTex(
            r"A\mathbf{v}_2 = \begin{bmatrix}3&1\\0&2\end{bmatrix}\begin{bmatrix}-1\\1\end{bmatrix} = \begin{bmatrix}-2\\2\end{bmatrix}",
            font_size=30,
        ).next_to(ver2_title, DOWN, buff=0.35, aligned_edge=LEFT)
        ver2b = MathTex(
            r"2\mathbf{v}_2 = 2\begin{bmatrix}-1\\1\end{bmatrix} = \begin{bmatrix}-2\\2\end{bmatrix}",
            font_size=30,
        ).next_to(ver2a, DOWN, buff=0.35, aligned_edge=LEFT)
        check2 = MathTex(r"\checkmark \text{ Matches!}", font_size=32, color=GREEN).next_to(ver2b, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(ver2_title), run_time=0.5)
        self.play(Write(ver2a), run_time=1.5)
        self.wait(0.5)
        self.play(Write(ver2b), run_time=1.5)
        self.play(FadeIn(check2, scale=1.3), run_time=0.5)
        self.wait(1.5)

        # Clear and show interpretation
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        interp_title = Text("Geometric Interpretation", font_size=36, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)

        interp_items = VGroup(
            MathTex(r"\lambda = 3", r"\text{: x-axis stretched 3×}", font_size=30, color=V1_COLOR),
            MathTex(r"\lambda = 2", r"\text{: direction } (-1,1) \text{ stretched 2×}", font_size=30, color=V2_COLOR),
            MathTex(r"\lambda < 0", r"\text{: would flip through origin}", font_size=30, color=RED_B),
            MathTex(r"\lambda = 0", r"\text{: collapses to origin (null space)}", font_size=30, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.3)

        self.play(Write(interp_title), run_time=0.8)
        for item in interp_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.5)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)


# ════════════════════════════════════════════════════════════════════
# SCENE 6 — Summary & Credits (~30 s)
# ════════════════════════════════════════════════════════════════════
class Scene6_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        dur = DURATIONS.get("scene6", 30)

        title = Text("Key Takeaways", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        takeaways = VGroup(
            Text("1. Eigenvectors are directions unchanged by a\n    linear transformation — only scaled.",
                 font_size=26, color=GREEN_B, line_spacing=1.2),
            Text("2. Eigenvalues come from solving\n    det(A − λI) = 0.",
                 font_size=26, color=YELLOW, line_spacing=1.2),
            Text("3. Eigenvectors come from the null space of\n    (A − λI) for each eigenvalue.",
                 font_size=26, color=V2_COLOR, line_spacing=1.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.3)

        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.5)

        self.wait(1.0)

        # Clear and show credits
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        credits_title = Text("Credits & References", font_size=36, color=BLUE_C, weight=BOLD).to_edge(UP, buff=0.5)
        
        student_info = VGroup(
            Text("ARADHYA", font_size=28, color=WHITE, weight=BOLD),
            Text("Student ID: e25b070764", font_size=22, color=YELLOW, weight=BOLD),
            Text("M3 Internal Assessment – Animation Video", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.12).shift(UP * 1.5)

        # Left box: References
        ref_header = Text("References:", font_size=22, color=BLUE_C, weight=BOLD)
        ref_items = VGroup(
            Text("• Gilbert Strang, Introduction to Linear Algebra", font_size=16, color=WHITE),
            Text("• David C. Lay, Linear Algebra & Applications", font_size=16, color=WHITE),
            Text("• 3Blue1Brown, Essence of Linear Algebra", font_size=16, color=WHITE),
            Text("• Manim Community Documentation", font_size=16, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ref_box = VGroup(ref_header, ref_items).arrange(DOWN, aligned_edge=LEFT, buff=0.15).shift(LEFT * 3.5 + DOWN * 0.8)

        # Right box: AI Disclosure
        ai_header = Text("AI Disclosure:", font_size=22, color=V2_COLOR, weight=BOLD)
        ai_items = VGroup(
            Text("Script, animation code and narration were", font_size=16, color=GREY_B),
            Text("produced with the help of Claude (Anthropic)", font_size=16, color=GREY_B),
            Text("inside Antigravity.", font_size=16, color=GREY_B),
            Text("Voice: edge-tts (en-GB-RyanNeural).", font_size=16, color=YELLOW),
            Text("All mathematics was checked by the student.", font_size=16, color=WHITE, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ai_box = VGroup(ai_header, ai_items).arrange(DOWN, aligned_edge=LEFT, buff=0.15).shift(RIGHT * 3.4 + DOWN * 0.8)

        self.play(Write(credits_title), FadeIn(student_info), run_time=1.0)
        self.play(FadeIn(ref_box), FadeIn(ai_box), run_time=1.5)

        if self.renderer.time < dur:
            self.wait(dur - self.renderer.time)
