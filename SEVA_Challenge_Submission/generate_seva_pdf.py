"""
Converts SEVA_FIRST_CHALLENGE_APPLICATION.md into a styled HTML file and
renders it to PDF ('SEVA Innovations Challange.pdf' and 'SEVA Innovations Challenge.pdf')
in both the root workspace and ARM AAA/ARM directory.
"""
import os
import re
import subprocess
import shutil
from pathlib import Path

WORKSPACE_ROOT = Path(r"C:\Users\user\Downloads\ARM AAA-20261118T161422Z-1-001")
PROJECT_DIR = WORKSPACE_ROOT / "ARM AAA" / "ARM"
MD_PATH = PROJECT_DIR / "SEVA_FIRST_CHALLENGE_APPLICATION.md"
HTML_PATH = PROJECT_DIR / "SEVA_Innovations_Challange.html"

PDF_TARGETS = [
    WORKSPACE_ROOT / "SEVA Innovations Challange.pdf",
    WORKSPACE_ROOT / "SEVA Innovations Challenge.pdf",
    PROJECT_DIR / "SEVA Innovations Challange.pdf",
    PROJECT_DIR / "SEVA Innovations Challenge.pdf",
]

def md_to_html(md_text: str) -> str:
    # Simple, clean markdown-to-HTML converter for our structured document
    lines = md_text.splitlines()
    html_lines = []
    in_code = False
    in_list = False
    in_table = False

    def format_inline(text: str) -> str:
        # Clean LaTeX formulas into crisp Unicode chemical formulas before HTML escaping
        replacements = [
            (r"\text{P}_2\text{O}_5", "P₂O₅"),
            (r"\text{K}_2\text{O}", "K₂O"),
            (r"\text{ZnSO}_4 \cdot 7\text{H}_2\text{O}", "ZnSO₄·7H₂O"),
            (r"\text{CaSO}_4 \cdot 2\text{H}_2\text{O}", "CaSO₄·2H₂O"),
            (r"\text{CaCO}_3", "CaCO₃"),
            (r"\text{N}_2\text{O}", "N₂O"),
            (r"\text{N}_{\text{DAP}}", "N_DAP"),
            (r"\text{ZnSO}_4", "ZnSO₄"),
            (r"\max(0, \text{Field N} - \text{N}_{\text{DAP}})", "max(0, Field N − N_DAP)"),
            (r"\rightarrow", "→"),
            (r"\times", "×"),
            (r"\\%", "%"),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)
        text = text.replace("$", "")
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # bold
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        # italic
        text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
        # inline code
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        return text

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not in_code:
                html_lines.append('<div class="portal-box">')
                in_code = True
            else:
                html_lines.append("</div>")
                in_code = False
            continue

        if in_code:
            html_lines.append(f"<p class='portal-text'>{format_inline(line)}</p>")
            continue

        if stripped.startswith("|"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if "---" in stripped:
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                html_lines.append("<table><thead><tr>")
                for c in cells:
                    html_lines.append(f"<th>{format_inline(c)}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
            else:
                html_lines.append("<tr>")
                for c in cells:
                    html_lines.append(f"<td>{format_inline(c)}</td>")
                html_lines.append("</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False

        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if stripped == "---":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<hr/>")
            continue

        if stripped.startswith("# "):
            html_lines.append(f"<h1>{format_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{format_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{format_inline(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4>{format_inline(stripped[5:])}</h4>")
        elif stripped.startswith("> "):
            html_lines.append(f"<div class='note-box'>{format_inline(stripped[2:])}</div>")
        elif stripped.startswith("- ") or re.match(r"^\d+\.\s+", stripped):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = re.sub(r"^(-\s+|\d+\.\s+)", "", stripped)
            html_lines.append(f"<li>{format_inline(content)}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{format_inline(stripped)}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_table:
        html_lines.append("</tbody></table>")

    body = "\n".join(html_lines)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SEVA Innovations Challange - Krishi Mitra (01 to 10)</title>
<style>
  @page {{
    size: A4;
    margin: 16mm 15mm 16mm 15mm;
  }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #0F172A;
    line-height: 1.55;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    color: #0B192C;
    font-size: 18pt;
    border-bottom: 3px solid #D4AF37;
    padding-bottom: 8px;
    margin-top: 0;
  }}
  h2 {{
    color: #FFFFFF;
    background-color: #0B192C;
    border-left: 6px solid #D4AF37;
    padding: 8px 12px;
    font-size: 13.5pt;
    margin-top: 22px;
    margin-bottom: 8px;
    border-radius: 4px;
    page-break-after: avoid;
  }}
  h3 {{
    color: #1E3E62;
    font-size: 11.5pt;
    margin-top: 12px;
    margin-bottom: 6px;
    border-bottom: 1px solid #CBD5E1;
    padding-bottom: 3px;
    page-break-after: avoid;
  }}
  h4 {{
    color: #0B192C;
    font-size: 10.5pt;
    margin-top: 10px;
    margin-bottom: 4px;
  }}
  p {{
    margin: 6px 0;
    text-align: justify;
  }}
  ul {{
    margin: 6px 0 10px 20px;
    padding: 0;
  }}
  li {{
    margin-bottom: 5px;
    text-align: justify;
  }}
  .portal-box {{
    background-color: #FEFCE8;
    border: 2px solid #D4AF37;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 8px 0 14px 0;
    page-break-inside: avoid;
  }}
  .portal-text {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    color: #0B192C;
    margin: 0;
    text-align: left;
    line-height: 1.45;
  }}
  .note-box {{
    background-color: #F1F5F9;
    border-left: 4px solid #1E3E62;
    padding: 6px 12px;
    font-size: 9.5pt;
    margin: 4px 0;
  }}
  code {{
    background-color: #F1F5F9;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: 'Consolas', monospace;
    font-size: 9.5pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #CBD5E1;
    padding: 6px 8px;
    text-align: left;
  }}
  th {{
    background-color: #0B192C;
    color: #FFFFFF;
  }}
  hr {{
    border: 0;
    border-top: 1px solid #CBD5E1;
    margin: 16px 0;
  }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

def main():
    md_text = MD_PATH.read_text(encoding="utf-8")
    html_content = md_to_html(md_text)
    HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"Created HTML at: {HTML_PATH}")

    # Find Microsoft Edge or Chrome to render high-quality PDF with Unicode scripts
    browser_Candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    browser_exe = None
    for b in browser_Candidates:
        if os.path.exists(b):
            browser_exe = b
            break

    primary_pdf = PDF_TARGETS[0]
    if browser_exe:
        print(f"Rendering PDF using: {browser_exe}")
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={primary_pdf}",
            HTML_PATH.as_uri()
        ]
        subprocess.run(cmd, check=True)
    else:
        raise RuntimeError("No headless browser found for PDF generation")

    if primary_pdf.exists() and primary_pdf.stat().st_size > 0:
        for target in PDF_TARGETS[1:]:
            shutil.copy2(primary_pdf, target)
            print(f"Copied PDF to: {target} ({target.stat().st_size} bytes)")
        print(f"SUCCESS: Primary PDF created at {primary_pdf} ({primary_pdf.stat().st_size} bytes)")
    else:
        raise RuntimeError("PDF generation failed")

if __name__ == "__main__":
    main()
