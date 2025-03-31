from fpdf import FPDF

def generate_pdf(scan_results, output_filename="scan_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "ZeroX Analyser Scan Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", style='', size=12)
    
    if not scan_results:
        pdf.cell(200, 10, "No vulnerabilities found.", ln=True, align='C')
    else:
        for result in scan_results:
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, f"File: {result['path']}", ln=True)
            
            pdf.set_font("Arial", style='', size=11)
            pdf.multi_cell(0, 8, f"Vulnerability: {result['name']}")
            pdf.multi_cell(0, 8, f"Line: {result['line_number']}")
            pdf.multi_cell(0, 8, f"Code Snippet: {result['code']}")
            pdf.ln(5)
            pdf.cell(0, 0, '-' * 100, ln=True)
            pdf.ln(5)
    
    pdf.output(output_filename)
    print(f"PDF report generated: {output_filename}")
