from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import os, requests, json
import sys
import json
import os
import time
import random
from datetime import datetime
from fpdf import FPDF

# Define styles for the PDF document
parrafo_style = {"size": 12, "align": "J", "line_height": 1.5}
titulo_style = {"size": 20, "style": "B", "align": "C"}
subtitulo_style = {"size": 16, "style": "B", "align": "L"}
nombre_archivo_style = {"size": 14, "align": "L"}
nombre_autor_style = {"size": 12, "align": "L"}

# Define a function to add text to the PDF with a given style
def add_text_to_pdf(pdf, text, style):
    pdf.set_font("Arial", style.get("style", ""), style.get("size", 12))
    pdf.set_text_color(0, 0, 0)  # Set text color to black
    if "align" in style:
        pdf.multi_cell(
            0, style.get("line_height", 5), txt=text, align=style["align"]
        )
    else:
        pdf.multi_cell(0, style.get("line_height", 5), txt=text)

# Add header information to the PDF
def add_header(pdf, username):
    # Add a sample logo
    pdf.image(
        "images/logo.png",
        x=10,
        y=8,
        w=33,
        h=33,
        type="PNG",
        link="",
    )
    pdf.ln(30)

    # Add information about the file name
    add_text_to_pdf(
        pdf,
        f"Report for username: {username}",
        nombre_archivo_style,
    )
    pdf.ln(10)
    add_text_to_pdf(
        pdf,
        f"Created on: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        nombre_archivo_style,
    )
    pdf.ln(10)

# Add an introduction text to the PDF
def add_introduction(pdf):
    introduccion = """
    This document presents a comprehensive analysis of the information collected, focusing on the potential risks to security and privacy. The data presented herein has been gathered from various open sources available on the internet.
    """
    add_text_to_pdf(pdf, introduccion, parrafo_style)
    pdf.ln(10)

# Add a section title to the PDF
def add_section_title(pdf, title):
    add_text_to_pdf(pdf, title, subtitulo_style)
    pdf.ln(5)

# Add important data information to the PDF
def add_important_data(pdf, data):
    for red_social, detalles in data.items():
        add_text_to_pdf(pdf, f"Social Media: {red_social}", parrafo_style)
        
        # Ensure 'status' is a dictionary
        if isinstance(detalles["status"], dict):
            add_text_to_pdf(
                pdf, f"Username: {detalles['status'].get('username', 'N/A')}", parrafo_style
            )
        else:
            add_text_to_pdf(
                pdf, f"Status: {detalles['status']}", parrafo_style
            )
        
        add_text_to_pdf(
            pdf, f"URL: {detalles.get('url_user', 'N/A')}", parrafo_style
        )
        add_text_to_pdf(
            pdf, f"Critical Level: {detalles.get('critical_level', 'N/A')}", parrafo_style
        )

        for recommendation in detalles.get("recommendations", []):
            add_text_to_pdf(
                pdf,
                f"Recommendation: {recommendation.get('recomendacion', 'N/A')}",
                parrafo_style,
            )
            add_text_to_pdf(
                pdf, f"Impact: {recommendation.get('impacto', 'N/A')}", parrafo_style
            )
        pdf.ln(5)

def add_breach_data(pdf, data):
    for entry in data:
        add_text_to_pdf(
            pdf, f"Email: {entry['Email']}", parrafo_style
        )
        add_text_to_pdf(
            pdf, f"Breaches: {', '.join(entry['Breaches'])}", parrafo_style
        )
        add_text_to_pdf(pdf, f"Password: {entry['Password']}", parrafo_style)
        add_text_to_pdf(
            pdf, f"Last Breach: {entry['Last Breach']}", parrafo_style
        )
        add_text_to_pdf(
            pdf, f"Critical Level: {entry['Nivel de Criticidad']}", parrafo_style
        )
        for recomendacion in entry["Recomendaciones"]:
            add_text_to_pdf(
                pdf, f"Recommendation: {recomendacion['recomendacion']}", parrafo_style
            )
            add_text_to_pdf(
                pdf, f"Impact: {recomendacion['impacto']}", parrafo_style
            )
        pdf.ln(5)

def generar_report_username(data):
    # Verify if there is data to generate the report
    if not data:
        print("No data available to generate the report.")
        return

    # Get the username from the first set of data
    username = list(data.keys())[0]
    # Create the PDF
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.add_font('Arial', '', '/Users/andrewbulthuis/Documents/GitHub/infohunt/arial.ttf', uni=True)

    # Add the header
    add_header(pdf, username)

    # Add the introduction
    add_introduction(pdf)

    # Add the section title for important data
    add_section_title(pdf, "Important Data")

    # Add information about the important data
    add_important_data(pdf, data)

    # Save the PDF
    pdf.output(f"output/report_{username}.pdf")
    print(f"PDF report generated: output/report_{username}.pdf")

def generar_report_email(data, email:str):
    # Verify if there is data to generate the report
    if not data:
        print("No data available to generate the report.")
        return

    # Create the PDF
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()

    # Add the header
    add_header(pdf, email)

    # Add the introduction
    add_introduction(pdf)

    # Add the section title for data breach information
    add_section_title(pdf, "Data Breach Information")

    # Add information about the data breach
    add_breach_data(pdf, data)

    # Save the PDF
    pdf.output(f"output/report_{email}.pdf")
    print(f"PDF report generated: output/report_{email}.pdf")


def generar_report_mail(informe_data):
    # Path where the PDF file will be saved
    output_path = "output"
    pdf_filename = os.path.join(output_path, "Informe_OSINT.pdf")

    # Create a PDF file
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Define custom colors
    colores = {
        "titulo": colors.darkblue,
        "subtitulo": colors.darkcyan,
        "parrafo": colors.black,
    }

    # Paragraph style for titles
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        name="TituloStyle", fontSize=24, textColor=colores["titulo"]
    )
    subtitulo_style = ParagraphStyle(
        name="SubtituloStyle", fontSize=16, textColor=colores["subtitulo"]
    )

    # Custom paragraph style
    parrafo_style = ParagraphStyle(
        name="ParrafoStyle", fontSize=12, leading=14, textColor=colores["parrafo"]
    )

    # Create the report content
    contenido = []

    # Custom paragraph style for centered title
    titulo_centrado_style = ParagraphStyle(
        name="TituloCentradoStyle",
        fontSize=24,
        textColor=colores["titulo"],
        alignment=1,
    )

    # Centered title
    contenido.append(
        Paragraph(
            '<font size="24" color="DarkBlue">OSINT Evaluation Report</font>',
            titulo_centrado_style,
        )
    )
    contenido.append(Spacer(1, 40))  # Increase vertical space

    # Evaluation details with boxes and more vertical space
    for item in informe_data:
        contenido.append(
            Paragraph("<b>Email:</b> {}".format(item["Email"]), parrafo_style)
        )
        contenido.append(
            Paragraph("<b>Source:</b> {}".format(item["Breaches"]), parrafo_style)
        )
        contenido.append(
            Paragraph("<b>Password:</b> {}".format(item["Password"]), parrafo_style)
        )
        contenido.append(
            Paragraph(
                "<b>Critical Level:</b> {}".format(item["Nivel de Criticidad"]),
                parrafo_style,
            )
        )

        # Indent recommendations
        recomendaciones = item["Recomendaciones"]  # Get the list of recommendations
        contenido.append(Paragraph("<b>Recommendations:</b>", parrafo_style))
        # contenido.append(Spacer(1, 5))  # Increase vertical space
        for recomendacion_info in recomendaciones:
            recomendacion = recomendacion_info["recomendacion"]

            # Format the recommendation with the impact
            recomendacion_formateada = f"&nbsp;&nbsp;&nbsp;&nbsp;- {recomendacion}"

            # Add the recommendation to the report content
            contenido.append(Paragraph(recomendacion_formateada, parrafo_style))
            contenido.append(
                Paragraph(
                    f'&nbsp;&nbsp;&nbsp;&nbsp;Impact Level: {recomendacion_info["impacto"]}',
                    parrafo_style,
                )
            )

            contenido.append(Spacer(1, 5))  # Increase vertical space
        contenido.append(Spacer(1, 10))  # Increase vertical space

    # Build the PDF
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)


def generar_report_username(datos_importantes):
    # Path where the PDF file will be saved
    output_path = "output"
    pdf_filename = os.path.join(output_path, "Informe_OSINT.pdf")

    # Create a PDF file
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Define custom colors
    colores = {
        "titulo": colors.darkblue,
        "subtitulo": colors.darkcyan,
        "parrafo": colors.black,
    }

    # Paragraph style for titles
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        name="TituloStyle", fontSize=24, textColor=colores["titulo"]
    )
    subtitulo_style = ParagraphStyle(
        name="SubtituloStyle", fontSize=16, textColor=colores["subtitulo"]
    )

    # Custom paragraph style
    parrafo_style = ParagraphStyle(
        name="ParrafoStyle", fontSize=12, leading=14, textColor=colores["parrafo"]
    )

    # Custom bold text style
    negrita_style = ParagraphStyle(
        name="NegritaStyle",
        fontSize=12,
        leading=14,
        textColor=colores["parrafo"],
        fontName="Helvetica-Bold",
    )

    # Create the report content
    contenido = []

    # Custom paragraph style for centered title
    titulo_centrado_style = ParagraphStyle(
        name="TituloCentradoStyle",
        fontSize=24,
        textColor=colores["titulo"],
        alignment=1,
    )

    # Centered title
    contenido.append(
        Paragraph(
            '<font size="24" color="DarkBlue">OSINT Evaluation Report</font>',
            titulo_centrado_style,
        )
    )
    contenido.append(Spacer(1, 40))  # Increase vertical space

    # Iterate over the important data and add it to the report
    for red_social, detalles in datos_importantes.items():
        # Social media title
        contenido.append(Paragraph(f"{red_social}", subtitulo_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space

        # User status and URL
        contenido.append(
            Paragraph(
                f'<b>Username:</b> {detalles["status"]["username"]}', parrafo_style
            )
        )
        contenido.append(
            Paragraph(f'<b>User URL:</b> {detalles["url_user"]}', parrafo_style)
        )

        # Critical level
        contenido.append(
            Paragraph(
                f'<b>Critical Level:</b> {detalles["nivel_critico"]}', parrafo_style
            )
        )

        # IDs (if available)
        ids = detalles["status"].get("ids")
        if ids:
            contenido.append(Paragraph("<b>IDs:</b>", parrafo_style))
            for key, value in ids.items():
                contenido.append(
                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{key}: {value}", parrafo_style)
                )

        try:
            # Image (if available)
            imagen_url = detalles["status"]["ids"].get("image")
            response = requests.get(imagen_url)
            if response.status_code == 200:
                # Convert the response to a BytesIO image object
                imagen_bytesio = BytesIO(response.content)

                # Load the image from BytesIO
                imagen = Image(imagen_bytesio, width=100, height=100)

                # Add the image to the report content
                contenido.append(imagen)
            # if imagen_url:
            #    imagen = Image(imagen_url, width=100, height=100)
            #    contenido.append(imagen)
        except:
            pass

        # Recommendations
        # contenido.append(Spacer(1, 5))  # Increase vertical space
        contenido.append(Paragraph("<b>Recommendations:</b>", parrafo_style))
        contenido.append(Spacer(1, 5))  # Increase vertical space
        for recomendacion_info in detalles["recomendaciones"]:
            recomendacion = recomendacion_info["recomendacion"]
            impacto = recomendacion_info["impacto"]
            # Indent the recommendation
            recomendacion_formateada = "&nbsp;&nbsp;&nbsp;&nbsp;- {}".format(
                recomendacion
            )
            contenido.append(Paragraph(f" {recomendacion_formateada}", parrafo_style))
            contenido.append(
                Paragraph(
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Impact Level: {impacto}",
                    parrafo_style,
                )
            )
            contenido.append(Spacer(1, 5))  # Increase vertical space

        contenido.append(Spacer(1, 20))  # Increase vertical space

    # Build the PDF
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)

def generar_report_domain(data, domain):
    # Path where the PDF file will be saved
    output_path = "output"
    pdf_filename = os.path.join(output_path, "Informe_OSINT.pdf")

    # Create a PDF file
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Define custom colors
    colores = {
        "titulo": colors.darkblue,
        "subtitulo": colors.darkcyan,
        "parrafo": colors.black,
    }

    # Paragraph style for titles
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        name="TituloStyle", fontSize=24, textColor=colores["titulo"]
    )
    subtitulo_style = ParagraphStyle(
        name="SubtituloStyle", fontSize=16, textColor=colores["subtitulo"]
    )
    titulo_seccion_style = ParagraphStyle(
        name="TituloSeccionStyle", fontSize=16, textColor=colors.darkblue, alignment=0
    )

    # Custom paragraph style
    parrafo_style = ParagraphStyle(
        name="ParrafoStyle", fontSize=12, leading=14, textColor=colores["parrafo"]
    )

    # Create the report content
    contenido = []

    # Custom paragraph style for centered title
    titulo_centrado_style = ParagraphStyle(
        name="TituloCentradoStyle",
        fontSize=24,
        textColor=colores["titulo"],
        alignment=1,
    )

    # Centered title
    contenido.append(
        Paragraph(
            '<font size="24" color="DarkBlue">OSINT Evaluation Report</font>',
            titulo_centrado_style,
        )
    )
    contenido.append(Spacer(1, 40))  # Increase vertical space

    # Add PyHunter information
    contenido.append(
        Paragraph("<b>Domain:</b> {}".format(data["domain"]), parrafo_style)
    )
    contenido.append(
        Paragraph(
            "<b>Organization Name:</b> {}".format(data["organization"]),
            parrafo_style,
        )
    )
    contenido.append(
        Paragraph("<b>Alexa Rank:</b> {}".format(data["alexa_rank"]), parrafo_style)
    )
    contenido.append(
        Paragraph("<b>Description:</b> {}".format(data["description"]), parrafo_style)
    )
    contenido.append(
        Paragraph("<b>Industry:</b> {}".format(data["industry"]), parrafo_style)
    )
    contenido.append(
        Paragraph("<b>Country:</b> {}".format(data["country"]), parrafo_style)
    )
    contenido.append(Paragraph("<b>City:</b> {}".format(data["city"]), parrafo_style))
    contenido.append(
        Paragraph("<b>Postal Code:</b> {}".format(data["postal_code"]), parrafo_style)
    )
    contenido.append(
        Paragraph("<b>Address:</b> {}".format(data["street"]), parrafo_style)
    )

    contenido.append(Spacer(1, 20))  # Increase vertical space

    # Add contact information
    contenido.append(Paragraph("<b>Contact Information:</b>", subtitulo_style))
    contenido.append(Spacer(1, 10))  # Increase vertical space
    for email_info in data["emails"]:
        contenido.append(
            Paragraph(
                "<b>Name:</b> {} {}".format(
                    email_info["first_name"], email_info["last_name"]
                ),
                parrafo_style,
            )
        )
        contenido.append(
            Paragraph("<b>Email:</b> {}".format(email_info["value"]), parrafo_style)
        )
        contenido.append(
            Paragraph(
                "<b>Confidence:</b> {}%".format(email_info["confidence"]), parrafo_style
            )
        )
        contenido.append(
            Paragraph(
                "<b>Source:</b> {}".format(email_info["sources"][0]["domain"]),
                parrafo_style,
            )
        )
        # Add social media information if available
        if email_info.get("linkedin"):
            contenido.append(
                Paragraph(
                    '<b>LinkedIn:</b> <a href="{}">{}</a>'.format(
                        email_info["linkedin"], email_info["linkedin"]
                    ),
                    parrafo_style,
                )
            )
        if email_info.get("twitter"):
            contenido.append(
                Paragraph(
                    '<b>Twitter:</b> <a href="{}">{}</a>'.format(
                        email_info["twitter"], email_info["twitter"]
                    ),
                    parrafo_style,
                )
            )
        # Add phone information if available
        if email_info.get("phone_number"):
            contenido.append(
                Paragraph(
                    "<b>Phone:</b> {}".format(email_info["phone_number"]),
                    parrafo_style,
                )
            )
        contenido.append(Spacer(1, 10))  # Increase vertical space

    # Add links to organization's social media
    contenido.append(
        Paragraph(
            "<b>Links to Organization's Social Media:</b>", subtitulo_style
        )
    )
    contenido.append(Spacer(1, 10))  # Increase vertical space
    if data["twitter"]:
        contenido.append(
            Paragraph(
                '<b>Twitter:</b> <a href="{}">{}</a>'.format(
                    data["twitter"], data["twitter"]
                ),
                parrafo_style,
            )
        )
    if data["facebook"]:
        contenido.append(
            Paragraph("<b>Facebook:</b> {}".format(data["facebook"]), parrafo_style)
        )
    if data["linkedin"]:
        contenido.append(
            Paragraph(
                '<b>LinkedIn:</b> <a href="{}">{}</a>'.format(
                    data["linkedin"], data["linkedin"]
                ),
                parrafo_style,
            )
        )
    if data["instagram"]:
        contenido.append(
            Paragraph("<b>Instagram:</b> {}".format(data["instagram"]), parrafo_style)
        )
    if data["youtube"]:
        contenido.append(
            Paragraph("<b>YouTube:</b> {}".format(data["youtube"]), parrafo_style)
        )

    # Add a page break to separate the pages
    contenido.append(PageBreak())

    contenido.append(Spacer(1, 40))  # Increase vertical space
    # General recommendations
    contenido.append(Paragraph("General Recommendations:", subtitulo_style))
    contenido.append(Spacer(1, 10))  # Increase vertical space

    recomendaciones_generales = [
        {
            "recomendacion": "Data Verification: Always verify the accuracy of the information before using it to make important decisions. Data can become outdated or inaccurate over time.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "Responsible Use: Use the information ethically and legally. Do not use it for malicious purposes, such as phishing or identity theft.",
            "impacto": "High",
        },
        {
            "recomendacion": "Data Security: If you handle personal data, make sure to follow best data security practices to protect the information from potential security breaches.",
            "impacto": "High",
        },
    ]

    for recomendacion_info in recomendaciones_generales:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(
            Paragraph(f"{recomendacion} (Impact: {impacto})", parrafo_style)
        )
        contenido.append(Spacer(1, 10))  # Increase vertical space

    contenido.append(Spacer(1, 40))  # Increase vertical space
    # Specific recommendations
    contenido.append(Paragraph("Specific Recommendations:", subtitulo_style))
    contenido.append(Spacer(1, 10))  # Increase vertical space

    recomendaciones_especificas = [
        {
            "recomendacion": "Social Media: Review the privacy settings on your social media accounts and adjust the visibility of your profiles and posts according to your preference.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "Secure Passwords: Use secure passwords and change them regularly. Enable two-factor authentication (2FA) when available to enhance the security of your accounts.",
            "impacto": "High",
        },
        {
            "recomendacion": "Sharing Personal Data: Avoid sharing personal or sensitive information in your online posts. Protect your privacy.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "Third-Party Applications: Be cautious when authorizing third-party applications on your social media accounts. Verify their reputation before granting access.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "Account Activity: Periodically review the activity on your accounts and adjust notification settings for greater control.",
            "impacto": "Low",
        },
        {
            "recomendacion": "Suspicious Messages: Be skeptical of suspicious messages you receive and do not click on unverified links.",
            "impacto": "High",
        },
    ]

    for recomendacion_info in recomendaciones_especificas:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(
            Paragraph(f"{recomendacion} (Impact: {impacto})", parrafo_style)
        )
        contenido.append(Spacer(1, 10))  # Increase vertical space

    # Load TheHarvester information
    theharvester_data = cargar_theharvester_json(domain)

    # Verify if it was successfully loaded
    if theharvester_data:

        # Add a page break to separate the sections
        contenido.append(PageBreak())

        # Add content from TheHarvester JSON
        contenido.append(Paragraph("TheHarvester Information:", styles["Heading2"]))

        # Add ASNs information
        contenido.append(Paragraph("ASNs:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(Paragraph(", ".join(theharvester_data["asns"]), parrafo_style))
        contenido.append(Spacer(1, 20))  # Increase vertical space

        # Add Emails information
        contenido.append(Paragraph("Emails:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(
            Paragraph(", ".join(theharvester_data["emails"]), parrafo_style)
        )
        contenido.append(Spacer(1, 20))  # Increase vertical space

        # Add Hosts information
        contenido.append(Paragraph("Hosts:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(
            Paragraph(", ".join(theharvester_data["hosts"]), parrafo_style)
        )
        contenido.append(Spacer(1, 20))  # Increase vertical space

        # Add interesting URLs information
        contenido.append(Paragraph("Interesting URLs:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(
            Paragraph(", ".join(theharvester_data["interesting_urls"]), parrafo_style)
        )
        contenido.append(Spacer(1, 20))  # Increase vertical space

        # Add IPs information
        contenido.append(Paragraph("IPs:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(Paragraph(", ".join(theharvester_data["ips"]), parrafo_style))
        contenido.append(Spacer(1, 20))  # Increase vertical space

        # Add Shodan information
        contenido.append(Paragraph("Shodan:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Increase vertical space
        contenido.append(
            Paragraph(", ".join(theharvester_data["shodan"]), parrafo_style)
        )
        contenido.append(Spacer(1, 40))  # Increase vertical space

    else:
        contenido.append(
            Paragraph(
                "No information from TheHarvester was found for the provided domain.",
                parrafo_style,
            )
        )

    recomendaciones_theharvester = [
        {
            "recomendacion": "ASNs: Investigate and verify the security of the ASNs associated with your domain.",
            "impacto": "High",
        },
        {
            "recomendacion": "Emails: Ensure that the email addresses associated with your domain are secure and protected against phishing.",
            "impacto": "High",
        },
        {
            "recomendacion": "Hosts: Perform a security analysis on the hosts used by your domain to detect potential vulnerabilities.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "Interesting URLs: Verify the security of the URLs you have identified as interesting for your domain.",
            "impacto": "Medium",
        },
        {
            "recomendacion": "IPs: Ensure that the IPs associated with your domain are properly configured and protected against attacks.",
            "impacto": "High",
        },
        {
            "recomendacion": "Shodan: Regularly monitor Shodan to ensure that no sensitive information is publicly exposed.",
            "impacto": "Low",
        },
    ]

    # Specific recommendations
    contenido.append(Paragraph("Specific Recommendations:", subtitulo_style))
    contenido.append(Spacer(1, 10))  # Increase vertical space

    for recomendacion_info in recomendaciones_theharvester:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(
            Paragraph(f"{recomendacion} (Impact: {impacto})", parrafo_style)
        )
        contenido.append(Spacer(1, 10))  # Increase vertical space

    # Build the PDF
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)


def addfooter(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    page_num_text = f"Page {doc.page}"
    page_width = letter[0]
    canvas.drawString(page_width - inch, 0.75 * inch, page_num_text)
    canvas.restoreState()


def add_header(canvas, doc):
    text = "InfoHUnter"
    canvas.setFont("Helvetica", 9)
    text_width = canvas.stringWidth(text, "Helvetica", 9)
    canvas.drawString(letter[0] - inch - text_width, letter[1] - 0.75 * inch, text)


def cargar_theharvester_json(domain):
    # Build the path to the JSON file
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        ruta_json = f"output/{domain}.json"
    else:
        ruta_json = f"output\\{domain}.json"

    # Verify if the JSON file exists
    if os.path.exists(ruta_json):
        # Load TheHarvester JSON file
        with open(ruta_json, "r") as json_file:
            theharvester_data = json.load(json_file)
        return theharvester_data
    else:
        print("The file " + ruta_json + " does not exist")
        return None
