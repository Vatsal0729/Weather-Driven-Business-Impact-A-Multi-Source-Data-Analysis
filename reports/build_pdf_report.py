import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

MD_PATH = r"C:\Users\vyasv\.gemini\antigravity\brain\b3a50ffe-df6a-4036-b560-a035c17603f4\project_report.md"
PDF_BRAIN_PATH = r"C:\Users\vyasv\.gemini\antigravity\brain\b3a50ffe-df6a-4036-b560-a035c17603f4\project_report.pdf"
PDF_WORKSPACE_PATH = r"C:\Users\vyasv\.gemini\antigravity\scratch\weather-business-impact-eda\reports\project_report.pdf"

# Ensure reports directory exists
os.makedirs(os.path.dirname(PDF_WORKSPACE_PATH), exist_ok=True)

with open(MD_PATH, "r", encoding="utf-8") as f:
    markdown_content = f.read()

# Colors (RGB)
NAVY = (15, 23, 42)        # #0F172A
SLATE = (51, 65, 85)       # #334155
LIGHT_BG = (248, 250, 252) # #F8FAFC
BORDER = (226, 232, 240)   # #E2E8F0
PRIMARY = (2, 132, 199)    # #0284C7 (Electric Blue)
ACCENT_GREEN = (16, 185, 129) # #10B981
TEXT_DARK = (30, 41, 59)   # #1E293B
MUTED = (100, 116, 139)    # #64748B

def clean_inline_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    return text.strip()

class EnterpriseReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(16, 16, 16)
        self.set_auto_page_break(auto=True, margin=18)
        
        # Load TrueType Unicode Fonts
        self.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
        self.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
        self.add_font("Arial", "I", r"C:\Windows\Fonts\ariali.ttf")
        self.add_font("Consolas", "", r"C:\Windows\Fonts\consola.ttf")
        self.add_font("Consolas", "B", r"C:\Windows\Fonts\consolab.ttf")
        
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Arial", "I", 7.5)
        self.set_text_color(*MUTED)
        self.set_xy(16, 8)
        self.cell(self.epw, 5, "Weather-Driven Business Intelligence Platform  |  Comprehensive Project Report", align="L")
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.line(16, 13, 16 + self.epw, 13)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.line(16, self.get_y(), 16 + self.epw, self.get_y())
        self.set_font("Arial", "", 7.5)
        self.set_text_color(*MUTED)
        self.set_y(-10)
        self.cell(self.epw / 2, 5, "Multi-Source Data Architecture & Econometric Regressions", align="L")
        self.cell(self.epw / 2, 5, f"Page {self.page_no()} of {{nb}}", align="R")

    def render_cover_page(self):
        self.add_page()
        
        # Top banner background
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 85, "F")
        
        # Accent stripe
        self.set_fill_color(*PRIMARY)
        self.rect(0, 83, 210, 3, "F")
        
        # Title text
        self.set_xy(18, 22)
        self.set_font("Arial", "B", 23)
        self.set_text_color(255, 255, 255)
        self.cell(self.epw, 10, "Weather-Driven Business Intelligence", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(18)
        self.set_font("Arial", "B", 17)
        self.set_text_color(*PRIMARY)
        self.cell(self.epw, 9, "A Multi-Source Real-Time Analysis Platform", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_xy(18, 48)
        self.set_font("Arial", "I", 10.5)
        self.set_text_color(203, 213, 225)
        self.multi_cell(self.epw, 6, "Comprehensive Architecture, Tech Stack, Econometric Regressions\n& Codebase Walkthrough (From Zero to Everything)")
        
        # Overview Card below banner
        self.set_xy(16, 96)
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.4)
        self.rect(16, 96, self.epw, 75, "FD")
        
        self.set_xy(22, 102)
        self.set_font("Arial", "B", 11)
        self.set_text_color(*NAVY)
        self.cell(self.epw - 12, 6, "Project Specification & Metadata", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        metadata_items = [
            ("Platform Name:", "Weather-Driven Business Intelligence (WDBI)"),
            ("GitHub Remote:", "https://github.com/Vatsal0729/Weather-Driven-Business-Impact..."),
            ("Primary Language:", "Python 3.13 (1,600+ Lines of Production Analytics)"),
            ("User Interface:", "Streamlit (Obsidian Dark Executive Theme)"),
            ("Econometric Engine:", "Two-Way Fixed Effects (TWFE) with HC1 Robust Standard Errors"),
            ("External Feeds:", "Open-Meteo Ground Telemetry, NASA POWER Satellite & NASA Worldview"),
            ("Revenue Connectors:", "Square POS API, Stripe Payments GMV & Custom CSV Importer"),
            ("Test Coverage:", "7/7 Automated Unit & Pipeline Integration Tests Passing")
        ]
        
        self.set_y(112)
        for label, val in metadata_items:
            self.set_x(22)
            self.set_font("Arial", "B", 8.5)
            self.set_text_color(*PRIMARY)
            self.cell(46, 5.8, label)
            self.set_font("Arial", "", 8.5)
            self.set_text_color(*TEXT_DARK)
            self.cell(self.epw - 58, 5.8, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
        # Table of Contents Summary
        self.set_xy(16, 180)
        self.set_font("Arial", "B", 12)
        self.set_text_color(*NAVY)
        self.cell(self.epw, 7, "Executive Summary & Report Structure", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        toc_items = [
            ("Part 1: The Big Idea", "The core business problem, real-world analogy, and core value proposition."),
            ("Part 2: Core Vocabulary", "40+ plain-English definitions across programming, data science, economics & weather."),
            ("Part 3: Technology Stack", "Library-by-library breakdown (Streamlit, Plotly, Pandas, Statsmodels, PyArrow)."),
            ("Part 4: Codebase Walkthrough", "Detailed inspection of all 7 production source files and architectures."),
            ("Part 5: Data Flow Architecture", "7-step end-to-end journey from synthetic factory to real-time dashboard."),
            ("Part 6: Automated Test Suite", "Verification protocol, test cases, and assertion logic."),
            ("Part 7: External Live APIs", "Open-Meteo, NASA POWER, NASA Worldview GIBS, Square POS & Stripe."),
            ("Part 8: Visual Design System", "High-contrast dark palette, white chart lines, and zero-overlap layout geometry."),
            ("Part 9: Version Control History", "Commit history and feature transitions across the development lifecycle."),
            ("Part 10: Comparative Benchmarks", "What standard academic projects do vs. what this platform accomplishes.")
        ]
        
        self.set_y(190)
        for title, desc in toc_items:
            self.set_x(18)
            self.set_font("Arial", "B", 8)
            self.set_text_color(*PRIMARY)
            self.cell(50, 5.2, title + " -")
            self.set_font("Arial", "", 8)
            self.set_text_color(*TEXT_DARK)
            self.cell(self.epw - 52, 5.2, desc, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
        self.set_y(260)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.line(16, 260, 16 + self.epw, 260)
        self.set_y(263)
        self.set_font("Arial", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(self.epw, 5, "Generated automatically from live platform documentation. October 2026.", align="C")

def build_pdf():
    pdf = EnterpriseReportPDF()
    pdf.alias_nb_pages()
    pdf.render_cover_page()
    
    # Start body on Page 2
    pdf.add_page()
    
    lines = markdown_content.split("\n")
    i = 0
    in_code = False
    code_lines = []
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        i += 1
        
        # Skip title headers since cover page handled them
        if i <= 3 and stripped.startswith("#"):
            continue
            
        # Code fence handling
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                # Render code block
                pdf.set_x(16)
                pdf.set_font("Consolas", "", 7.2)
                code_text = "\n".join(code_lines)
                
                # Background rect for code block
                lines_count = len(code_lines)
                block_height = lines_count * 4.2 + 6
                
                # If block exceeds page, let it break or handle
                if pdf.get_y() + block_height > 275:
                    pdf.add_page()
                    
                cur_y = pdf.get_y()
                pdf.set_fill_color(241, 245, 249) # #F1F5F9
                pdf.set_draw_color(203, 213, 225) # #CBD5E1
                pdf.set_line_width(0.3)
                pdf.rect(16, cur_y, pdf.epw, block_height, "FD")
                
                pdf.set_xy(19, cur_y + 3)
                pdf.set_text_color(15, 23, 42)
                for cl in code_lines:
                    pdf.set_x(19)
                    pdf.cell(pdf.epw - 6, 4.2, cl, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(3)
                code_lines = []
            continue
            
        if in_code:
            code_lines.append(line)
            continue
            
        # Table handling
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [clean_inline_md(c) for c in stripped.strip("|").split("|")]
            # Check if divider row like |:---|:---|
            if all(re.match(r"^:?-+:?$", c.strip()) for c in cells if c.strip()):
                continue
            if not in_table:
                in_table = True
                table_rows = [cells]
            else:
                table_rows.append(cells)
            continue
        else:
            if in_table and table_rows:
                # Flush table using fpdf2 table method
                num_cols = max(len(r) for r in table_rows)
                # Normalize rows
                norm_data = []
                for r in table_rows:
                    padded = (r + [""] * num_cols)[:num_cols]
                    norm_data.append(padded)
                    
                pdf.set_x(16)
                pdf.set_font("Arial", "", 7.5)
                
                # Check height and page break if needed
                if pdf.get_y() > 240:
                    pdf.add_page()
                    
                try:
                    if num_cols == 2:
                        widths = (48, pdf.epw - 48)
                    elif num_cols == 3:
                        widths = (44, 44, pdf.epw - 88)
                    elif num_cols == 4:
                        widths = (38, 38, 38, pdf.epw - 114)
                    else:
                        widths = tuple([pdf.epw / num_cols] * num_cols)
                        
                    with pdf.table(col_widths=widths, line_height=5.0, text_align="LEFT", borders_layout="SINGLE") as t:
                        for row_idx, row in enumerate(norm_data):
                            r = t.row()
                            if row_idx == 0:
                                pdf.set_font("Arial", "B", 7.5)
                                pdf.set_fill_color(224, 242, 254) # light sky blue
                                pdf.set_text_color(*NAVY)
                            else:
                                pdf.set_font("Arial", "", 7.2)
                                pdf.set_fill_color(255, 255, 255) if row_idx % 2 == 1 else pdf.set_fill_color(248, 250, 252)
                                pdf.set_text_color(*TEXT_DARK)
                            for val in row:
                                r.cell(val)
                except Exception as e:
                    # Fallback text rendering if table error
                    pdf.set_font("Arial", "", 7.5)
                    for r in norm_data:
                        pdf.set_x(16)
                        pdf.multi_cell(pdf.epw, 4.5, " | ".join(r))
                        
                pdf.ln(3)
                in_table = False
                table_rows = []
                
        # Horizontal Rule
        if re.match(r"^---+$", stripped):
            pdf.ln(2)
            pdf.set_draw_color(*BORDER)
            pdf.set_line_width(0.3)
            pdf.line(16, pdf.get_y(), 16 + pdf.epw, pdf.get_y())
            pdf.ln(3)
            continue
            
        # Section Header Level 2 (## Part ...)
        if stripped.startswith("## "):
            header_text = clean_inline_md(stripped[3:])
            if pdf.get_y() > 235:
                pdf.add_page()
            else:
                pdf.ln(4)
                
            pdf.set_x(16)
            pdf.set_fill_color(240, 249, 255) # light blue header bar
            pdf.set_draw_color(*PRIMARY)
            pdf.set_line_width(0.8)
            y_start = pdf.get_y()
            pdf.rect(16, y_start, pdf.epw, 8, "FD")
            
            pdf.set_xy(18, y_start + 1.2)
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(*PRIMARY)
            pdf.cell(pdf.epw - 4, 6, header_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
            continue
            
        # Section Header Level 3 (### Subheader)
        if stripped.startswith("### "):
            header_text = clean_inline_md(stripped[4:])
            if pdf.get_y() > 250:
                pdf.add_page()
            else:
                pdf.ln(2.5)
            pdf.set_x(16)
            pdf.set_font("Arial", "B", 9.5)
            pdf.set_text_color(*NAVY)
            pdf.cell(pdf.epw, 6, header_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
            continue
            
        # Section Header Level 4 (#### Header)
        if stripped.startswith("#### "):
            header_text = clean_inline_md(stripped[5:])
            if pdf.get_y() > 255:
                pdf.add_page()
            else:
                pdf.ln(1.5)
            pdf.set_x(16)
            pdf.set_font("Arial", "B", 8.8)
            pdf.set_text_color(*SLATE)
            pdf.cell(pdf.epw, 5, header_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
            continue
            
        # Blockquote (> text)
        if stripped.startswith(">"):
            quote_text = clean_inline_md(stripped.lstrip(">").strip())
            if not quote_text:
                continue
            if pdf.get_y() > 255:
                pdf.add_page()
            pdf.ln(1.5)
            y_q = pdf.get_y()
            pdf.set_font("Arial", "I", 8.2)
            
            # Measure height
            test_lines = pdf.multi_cell(pdf.epw - 10, 4.8, quote_text, dry_run=True, output="LINES")
            q_height = len(test_lines) * 4.8 + 4
            
            # Background & left accent border
            pdf.set_fill_color(248, 250, 252)
            pdf.rect(16, y_q, pdf.epw, q_height, "F")
            pdf.set_fill_color(*PRIMARY)
            pdf.rect(16, y_q, 1.8, q_height, "F")
            
            pdf.set_xy(20, y_q + 2)
            pdf.set_text_color(*TEXT_DARK)
            pdf.multi_cell(pdf.epw - 8, 4.8, quote_text)
            pdf.ln(2)
            continue
            
        # Bullet list items (- item or * item)
        if stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("• "):
            bullet_text = clean_inline_md(stripped[2:])
            if pdf.get_y() > 265:
                pdf.add_page()
            pdf.set_x(16)
            pdf.set_font("Arial", "B", 8)
            pdf.set_text_color(*PRIMARY)
            pdf.cell(4, 4.8, "•", new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_font("Arial", "", 8.2)
            pdf.set_text_color(*TEXT_DARK)
            pdf.multi_cell(pdf.epw - 5, 4.8, bullet_text)
            continue
            
        # Numbered list items (1. item)
        m_num = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if m_num:
            n_val, item_text = m_num.group(1), clean_inline_md(m_num.group(2))
            if pdf.get_y() > 265:
                pdf.add_page()
            pdf.set_x(16)
            pdf.set_font("Arial", "B", 8)
            pdf.set_text_color(*PRIMARY)
            pdf.cell(6, 4.8, f"{n_val}.", new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_font("Arial", "", 8.2)
            pdf.set_text_color(*TEXT_DARK)
            pdf.multi_cell(pdf.epw - 7, 4.8, item_text)
            continue
            
        # Empty line
        if not stripped:
            pdf.ln(1.5)
            continue
            
        # Regular paragraph text
        clean_p = clean_inline_md(stripped)
        if pdf.get_y() > 265:
            pdf.add_page()
        pdf.set_x(16)
        pdf.set_font("Arial", "", 8.2)
        pdf.set_text_color(*TEXT_DARK)
        pdf.multi_cell(pdf.epw, 4.8, clean_p)
        pdf.ln(1)
        
    # Flush any remaining table at the very end
    if in_table and table_rows:
        num_cols = max(len(r) for r in table_rows)
        norm_data = [(r + [""] * num_cols)[:num_cols] for r in table_rows]
        pdf.set_x(16)
        if num_cols == 2:
            widths = (48, pdf.epw - 48)
        else:
            widths = tuple([pdf.epw / num_cols] * num_cols)
        with pdf.table(col_widths=widths, line_height=5.0) as t:
            for row in norm_data:
                r = t.row()
                for val in row:
                    r.cell(val)

    # Save outputs to both Brain artifact directory and workspace reports folder
    pdf.output(PDF_BRAIN_PATH)
    pdf.output(PDF_WORKSPACE_PATH)
    print(f"Successfully generated PDF!")
    print(f"Brain Artifact Path: {PDF_BRAIN_PATH}")
    print(f"Workspace Path: {PDF_WORKSPACE_PATH}")
    print(f"Total Page Count: {pdf.page_no()}")

if __name__ == "__main__":
    build_pdf()
