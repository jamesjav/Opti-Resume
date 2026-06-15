import os
from PyPDF2 import PdfReader
from datetime import datetime

# Try reportlab first (Unicode/Chinese support), fall back to fpdf
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    from fpdf import FPDF


def ExtractPDF(file) -> str:
    """Extract text from an uploaded PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def CreatePDF(text: str, input_filename: str, language: str = "English") -> str | None:
    """
    Create a PDF from the optimized resume text.
    Uses reportlab for Unicode/Chinese support when available,
    falls back to fpdf otherwise.
    """
    os.makedirs("Artifacts", exist_ok=True)
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    file_name = f"{input_filename}_Optimized_{timestamp}.pdf"

    if HAS_REPORTLAB:
        return _create_pdf_reportlab(text, file_name, language)
    else:
        return _create_pdf_fpdf(text, file_name)


def _create_pdf_reportlab(text: str, file_name: str, language: str) -> str | None:
    """Create PDF using reportlab — full Unicode/Chinese support."""
    try:
        # Try to register a Chinese font
        chinese_font_registered = False
        font_name = "Helvetica"
        font_path_candidates = [
            "C:/Windows/Fonts/msyh.ttc",   # Microsoft YaHei
            "C:/Windows/Fonts/simsun.ttc",  # SimSun
            "C:/Windows/Fonts/simhei.ttf",  # SimHei
        ]
        for fpath in font_path_candidates:
            if os.path.exists(fpath):
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', fpath, subfontIndex=0))
                    font_name = 'ChineseFont'
                    chinese_font_registered = True
                    break
                except Exception:
                    continue

        if language == "Chinese" and not chinese_font_registered:
            # Fall back to fpdf if Chinese font not available
            return _create_pdf_fpdf(text, file_name)

        doc = SimpleDocTemplate(
            file_name,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            'ResumeText',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            leading=14,
            spaceAfter=4,
        )
        # Bold style for headings
        style_bold = ParagraphStyle(
            'ResumeBold',
            parent=style,
            fontName=font_name,
            fontSize=11,
            leading=16,
            spaceAfter=2,
            spaceBefore=8,
        )

        story = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
            elif line.isupper() or line.endswith(":"):
                # Likely a heading
                story.append(Paragraph(line, style_bold))
            else:
                story.append(Paragraph(line, style))

        doc.build(story)
        return file_name if os.path.exists(file_name) else None

    except Exception:
        return _create_pdf_fpdf(text, file_name)


def _create_pdf_fpdf(text: str, file_name: str) -> str | None:
    """Create PDF using fpdf — basic Latin-1 only (fallback)."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.set_margins(10, 10, 10)
        pdf.set_font("Courier", size=10)
        for line in text.split("\n"):
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), align='L')
        pdf.output(file_name, 'F')
        return file_name if os.path.exists(file_name) else None
    except Exception:
        return None
