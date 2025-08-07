from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import simpleSplit
from weasyprint import HTML

def convert_html_to_pdf(input_html_path: str, output_pdf_path: str):
    HTML(input_html_path).write_pdf(output_pdf_path)
    print(f"PDF generated at: {output_pdf_path}")

def html_to_pdf(html_file_path: str, output_pdf_path: str, font_size=12, margin=40):
    # Read and parse HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()

    # Setup PDF
    pdf = canvas.Canvas(output_pdf_path, pagesize=LETTER)
    width, height = LETTER
    y = height - margin

    pdf.setFont("Helvetica", font_size)

    # Split text into lines (wrapped to page width)
    lines = []
    for paragraph in text.split('\n'):
        paragraph = paragraph.strip()
        if paragraph:
            wrapped = simpleSplit(paragraph, "Helvetica", font_size, width - 2 * margin)
            lines.extend(wrapped + [''])  # Add line break after each paragraph

    # Write lines to PDF
    for line in lines:
        if y < margin:
            pdf.showPage()
            pdf.setFont("Helvetica", font_size)
            y = height - margin
        pdf.drawString(margin, y, line)
        y -= font_size + 2

    pdf.save()
    print(f"PDF generated at: {output_pdf_path}")
