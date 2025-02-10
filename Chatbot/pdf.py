import fpdf

def generate_report():
    pdf = fpdf.FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set up title
    pdf.set_font("Arial", style='B', size=18)
    pdf.cell(200, 10, "PATIENT SCREENING REPORT", ln=True, align='C')
    pdf.ln(10)  

    # Patient Details Section
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Patient Details", ln=True, border='B')
    pdf.set_font("Arial", size=12)
    pdf.ln(5)  

    # # Create a table for patient details
    # col_width = 95  
    # row_height = 10 
    # for key, value in patient_details.items():
    #     pdf.cell(col_width, row_height, key, border=1)
    #     pdf.cell(col_width, row_height, str(value), border=1, ln=True)
    # pdf.ln(10)  

    # Symptoms Summary Section
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Symptoms Summary", ln=True, border='B')
    pdf.set_font("Arial", size=12)
    pdf.ln(5) 

    # Define column widths for the symptoms table
    col_widths = [40, 30, 30, 40, 60]  
    headers = ["Symptom", "Frequency", "Severity", "Duration", "Additional Notes"]
    row_height = 10

    # Add table headers
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], row_height, header, border=1, align='C')
    pdf.ln(row_height)

    # # Add symptom data rows
    # for entry in patient_data:
    #     pdf.cell(col_widths[0], row_height, entry["Symptom"], border=1)
    #     pdf.cell(col_widths[1], row_height, entry["Frequency"], border=1)
    #     pdf.cell(col_widths[2], row_height, entry["Severity"], border=1)
    #     pdf.cell(col_widths[3], row_height, entry["Duration"], border=1)
    #     pdf.cell(col_widths[4], row_height, entry["Additional Notes"], border=1, ln=True)

    # Save the PDF
    pdf.output("filename.pdf")
    print(f"Patient report successfully saved as filename.pdf .")

generate_report()