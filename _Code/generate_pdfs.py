#!/usr/bin/env python3
"""Convert Markdown files to PDF using weasyprint."""
import markdown
import weasyprint
import os

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
@page { size: A4; margin: 2cm; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       font-size: 11pt; line-height: 1.6; color: #222; }
h1 { color: #1a1a2e; border-bottom: 2px solid #1a1a2e; padding-bottom: 6px; font-size: 20pt; }
h2 { color: #2d3436; font-size: 16pt; margin-top: 1.5em; }
h3 { color: #2d3436; font-size: 13pt; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background: #f0f0f0; }
code { background: #f5f5f5; padding: 2px 4px; border-radius: 3px; font-size: 10pt; }
pre { background: #f5f5f5; padding: 12px; border-radius: 5px; overflow-x: auto; font-size: 9pt; }
blockquote { border-left: 4px solid #1a1a2e; margin: 1em 0; padding: 0.5em 1em; background: #f9f9f9; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em 0; }
"""

FILES = {
    "Storyboard.md": "Storyboard.pdf",
    "Narration_Script.md": "Narration_Script.pdf",
    "Code_Walkthrough.md": "Code_Walkthrough.pdf",
    "Viva_Prep.md": "Viva_Prep.pdf",
}

for md_name, pdf_name in FILES.items():
    md_path = os.path.join(PROJ, md_name)
    pdf_path = os.path.join(PROJ, pdf_name)
    
    with open(md_path) as f:
        md_text = f.read()
    
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html}</body></html>"""
    
    weasyprint.HTML(string=full_html).write_pdf(pdf_path)
    print(f"✓ {md_name} → {pdf_name}")

print("\nAll PDFs generated!")
