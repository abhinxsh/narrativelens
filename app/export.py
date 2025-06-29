from fpdf import FPDF

def create_pdf_report(analysis_results, filename="narrative_lens_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "NarrativeLens Analysis Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    for idx, result in enumerate(analysis_results):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Article {idx+1}", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"Political Bias: {result.get('bias','')}")
        pdf.multi_cell(0, 8, f"Emotional Tone: {result.get('emotion','')}")
        pdf.multi_cell(0, 8, f"Framing Style: {result.get('framing','')}")
        pdf.multi_cell(0, 8, f"Omitted Perspectives:\n{result.get('omissions','')}")
        pdf.ln(5)

    pdf.output(filename)
