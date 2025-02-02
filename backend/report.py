from fpdf import FPDF

def generate_pdf_report(transcript: str, feedback: str, score: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "IELTS Speaking Test Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Transcription: {transcript}")
    pdf.multi_cell(0, 10, f"Feedback: {feedback}")
    pdf.multi_cell(0, 10, f"Score: {score}")
    pdf.output("report.pdf")