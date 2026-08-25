"""Convert PROJECT_DOCUMENTATION.md to a styled PDF using fpdf2 (pure Python, no native deps)."""
import re, textwrap
import markdown
from fpdf import FPDF

INPUT  = "PROJECT_DOCUMENTATION.md"
OUTPUT = "PROJECT_DOCUMENTATION.pdf"

# ── 1. Read markdown ──────────────────────────────────────────────────────
with open(INPUT, encoding="utf-8") as f:
    raw = f.read()

m = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
title = m.group(1) if m else "Project Documentation"
body_md = re.sub(r"^#\s+.+\n", "", raw, count=1)

# ── 2. Markdown → HTML ───────────────────────────────────────────────────
exts = ["toc", "tables", "fenced_code"]
html_body = markdown.markdown(body_md, extensions=exts,
    extension_configs={"toc": {"title": "Table of Contents", "toc_depth": 3}})

# ── 3. Strip HTML tags for fpdf2 (fpdf2 handles raw text, not HTML) ──────
def strip_tags(html):
    """Remove HTML tags, keeping text content."""
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

plain_text = strip_tags(html_body)

# ── 4. Build PDF with fpdf2 ──────────────────────────────────────────────
class DocPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=28)
        # Add Unicode font
        self.add_font("DejaVu", "", "C:/Windows/Fonts/arial.ttf", uni=True)
        self.add_font("DejaVu", "B", "C:/Windows/Fonts/arialbd.ttf", uni=True)
        self.add_font("DejaVu", "I", "C:/Windows/Fonts/ariali.ttf", uni=True)
        self.add_font("DejaVu", "BI", "C:/Windows/Fonts/arialbi.ttf", uni=True)

    def footer(self):
        if self.page_no() == 1:
            return  # No footer on cover page
        self.set_y(-15)
        self.set_font("DejaVu", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "AI-Powered Career Guidance System — Documentation", align="C")
        self.cell(0, 10, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")

    def cover_page(self):
        self.add_page()
        self.set_fill_color(15, 23, 42)  # #0f172a
        self.rect(0, 0, 210, 297, "F")

        # Brand
        self.set_y(70)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(96, 165, 250)
        self.cell(0, 10, "\u2726  PROJECT DOCUMENTATION", align="C", new_x="LMARGIN", new_y="NEXT")

        # Title
        self.ln(10)
        self.set_font("DejaVu", "B", 26)
        self.set_text_color(255, 255, 255)
        self.multi_cell(0, 12, title, align="C")

        # Subtitle
        self.ln(8)
        self.set_font("DejaVu", "", 11)
        self.set_text_color(203, 213, 225)
        self.multi_cell(0, 7,
            "Complete Project Documentation & Team Learning Guide\n"
            "Python | Django | MySQL | Ollama | Llama 3.2",
            align="C")

        # Meta at bottom
        self.set_y(230)
        self.set_draw_color(51, 65, 85)
        self.line(40, self.get_y(), 170, self.get_y())
        self.ln(8)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(148, 163, 184)
        self.multi_cell(0, 5,
            "Technology Stack: Python 3 | Django 6.0.7 | MySQL | Bootstrap 5 | ReportLab\n"
            "AI Engine: Ollama + Llama 3.2 (3B) | Version Control: Git + GitHub",
            align="C")

    def chapter_heading(self, text, level=1):
        """Render a heading with appropriate styling."""
        if level == 1:
            self.add_page()
            self.ln(4)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(15, 23, 42)
            self.multi_cell(0, 9, text)
            # Blue underline
            y = self.get_y() + 1
            self.set_draw_color(59, 130, 246)
            self.set_line_width(0.6)
            self.line(self.l_margin, y, 210 - self.r_margin, y)
            self.ln(6)
        elif level == 2:
            self.ln(4)
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(30, 58, 95)
            self.multi_cell(0, 7, text)
            self.ln(2)
        elif level == 3:
            self.ln(3)
            self.set_font("DejaVu", "B", 10.5)
            self.set_text_color(51, 65, 85)
            self.multi_cell(0, 6, text)
            self.ln(1)
        elif level == 4:
            self.ln(2)
            self.set_font("DejaVu", "BI", 10)
            self.set_text_color(71, 85, 105)
            self.multi_cell(0, 6, text)
            self.ln(1)

    def body_text(self, text, bold=False, italic=False):
        """Render normal body text."""
        style = ""
        if bold:
            style += "B"
        if italic:
            style += "I"
        self.set_font("DejaVu", style, 9.5)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 5.2, text)
        self.ln(1)

    def code_block(self, code):
        """Render a code block with background."""
        self.ln(2)
        self.set_fill_color(241, 245, 249)
        self.set_draw_color(226, 232, 240)
        x = self.l_margin
        w = 210 - self.l_margin - self.r_margin
        lines = code.split("\n")
        h = len(lines) * 4.2 + 6
        # Check if we need a page break
        if self.get_y() + h > 297 - 28:
            self.add_page()
        y0 = self.get_y()
        self.rect(x, y0, w, h, "DF")
        self.set_y(y0 + 3)
        self.set_x(x + 4)
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(51, 65, 85)
        for line in lines:
            self.set_x(x + 4)
            self.cell(w - 8, 4.2, line, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y0 + h + 3)

    def table_row(self, cells, is_header=False):
        """Render a single table row."""
        if is_header:
            self.set_font("DejaVu", "B", 8.5)
            self.set_fill_color(30, 58, 95)
            self.set_text_color(255, 255, 255)
        else:
            self.set_font("DejaVu", "", 8.5)
            self.set_text_color(30, 41, 59)
            self.set_fill_color(248, 250, 252)

        w = (210 - self.l_margin - self.r_margin) / len(cells)
        for cell in cells:
            self.cell(w, 6, str(cell)[:60], border=1, fill=is_header, align="L")
        self.ln()

    def hr(self):
        """Horizontal rule."""
        self.ln(3)
        y = self.get_y()
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(self.l_margin, y, 210 - self.r_margin, y)
        self.ln(4)

    def bullet(self, text, indent=0):
        """Render a bullet point."""
        x = self.l_margin + indent * 6
        self.set_x(x)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(30, 41, 59)
        self.cell(5, 5, "\u2022")
        self.set_font("DejaVu", "", 9)
        self.multi_cell(210 - self.r_margin - x - 5, 5, text)
        self.ln(0.5)


def parse_and_render(pdf, html):
    """Parse the HTML from markdown and render it into the PDF."""
    # Split HTML into elements
    lines = html.split("\n")
    in_pre = False
    pre_buf = []
    in_table = False
    table_rows = []
    table_header_done = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines (add spacing)
        if not line:
            if in_pre:
                pre_buf.append("")
            elif in_table:
                pass
            i += 1
            continue

        # Handle <pre><code> blocks
        if "<pre>" in line or "<pre><code>" in line:
            in_pre = True
            pre_buf = []
            i += 1
            continue
        if "</pre>" in line or "</code></pre>" in line:
            in_pre = False
            pdf.code_block("\n".join(pre_buf))
            i += 1
            continue
        if in_pre:
            # Strip code tags
            cleaned = re.sub(r"<[^>]+>", "", line)
            pre_buf.append(cleaned)
            i += 1
            continue

        # Handle tables
        if "<table>" in line:
            in_table = True
            table_rows = []
            table_header_done = False
            i += 1
            continue
        if "</table>" in line:
            in_table = False
            for ri, row in enumerate(table_rows):
                pdf.table_row(row, is_header=(ri == 0))
            pdf.ln(2)
            i += 1
            continue
        if in_table:
            if "<thead>" in line or "</thead>" in line or "<tbody>" in line or "</tbody>" in line:
                i += 1
                continue
            if "<tr>" in line:
                row_cells = []
                i += 1
                while i < len(lines) and "</tr>" not in lines[i]:
                    cl = lines[i].strip()
                    cell_text = re.sub(r"<[^>]+>", "", cl).strip()
                    if cell_text:
                        row_cells.append(cell_text)
                    i += 1
                table_rows.append(row_cells)
                i += 1
                continue

        # Handle headings
        h_match = re.match(r"<h([1-4])[^>]*>(.*?)</h\1>", line)
        if h_match:
            level = int(h_match.group(1))
            text = re.sub(r"<[^>]+>", "", h_match.group(2)).strip()
            if text:
                pdf.chapter_heading(text, level=level)
            i += 1
            continue

        # Handle <hr>
        if "<hr" in line:
            pdf.hr()
            i += 1
            continue

        # Handle <p> tags
        p_match = re.match(r"<p[^>]*>(.*?)</p>", line, re.DOTALL)
        if p_match:
            text = re.sub(r"<[^>]+>", "", p_match.group(1)).strip()
            if text:
                pdf.body_text(text)
            i += 1
            continue

        # Handle <li> tags
        if "<li>" in line or "<li " in line:
            text = re.sub(r"<[^>]+>", "", line).strip()
            if text:
                # Check nesting level
                indent = 0
                if lines[i].count("<ul") > 1 or lines[i].count("<ol") > 1:
                    indent = 1
                pdf.bullet(text, indent=indent)
            i += 1
            continue

        # Skip pure tag lines
        if re.match(r"^</?(ul|ol|li|p|div|span|blockquote|section|article|strong|em|a |a>|br|table|thead|tbody|tr|th|td|pre|code|h[1-6]|hr)", line, re.IGNORECASE):
            i += 1
            continue

        # Skip any remaining HTML tags
        if line.startswith("<") and line.endswith(">"):
            i += 1
            continue

        # Plain text fallback
        text = re.sub(r"<[^>]+>", "", line).strip()
        if text and len(text) > 1:
            # Check if it looks like a heading marker
            if text.startswith("# "):
                pdf.chapter_heading(text[2:], level=1)
            elif text.startswith("## "):
                pdf.chapter_heading(text[3:], level=2)
            elif text.startswith("### "):
                pdf.chapter_heading(text[4:], level=3)
            elif text.startswith("#### "):
                pdf.chapter_heading(text[5:], level=4)
            else:
                pdf.body_text(text)

        i += 1


# ── 5. Generate PDF ──────────────────────────────────────────────────────
print(f"Converting {INPUT} → {OUTPUT} ...")
pdf = DocPDF()
pdf.set_title(title)
pdf.set_author("AI Career Guidance Team")
pdf.cover_page()
parse_and_render(pdf, html_body)
pdf.output(OUTPUT)
print(f"Done! PDF saved to {OUTPUT} ({pdf.page_no()} pages)")
