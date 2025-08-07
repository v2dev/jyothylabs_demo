import requests
import difflib
import os
import smtplib
from email.message import EmailMessage
import mimetypes
import pdfkit
import html2text
# from html_to_pdf import html_to_pdf
from selenium_html_to_pdf import render_html_to_pdf

# ---- CONFIGURATION ----
URL = "https://example.com"  # Target URL to monitor
FILE_PATH = "./website-2/index.html"
OLD_FILE = "previous_content.html"
DIFF_HTML = "diff_output.html"
DIFF_PDF = "diff_output.pdf"
EMAIL_SENDER = "harshapaul@gmail.com"
EMAIL_RECEIVER = "harshapaul@gmail.com"
EMAIL_SUBJECT = "Webpage Change Detected"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "harshapaul@gmail.com"
SMTP_PASS = ""

# ---- STEP 1: Fetch current content ----
def fetch_page():
    response = requests.get(URL)
    response.raise_for_status()
    return response.text

# ---- STEP 1.1: Fetch current content from local----
def fetch_page_local():
    with open(FILE_PATH, "r") as file:
        content = file.read()
    return content

# ---- STEP 2: Load previous content and compare ----
def detect_change(new_content):
    if not os.path.exists(OLD_FILE):
        with open(OLD_FILE, "w", encoding='utf-8') as f:
            f.write(new_content)
        return None  # First run, no comparison

    with open(OLD_FILE, "r", encoding='utf-8') as f:
        old_content = f.read()

    if new_content == old_content:
        return None

    # Save new content
    with open(OLD_FILE, "w", encoding='utf-8') as f:
        f.write(new_content)

    # Generate diff
    old_lines = html2text.html2text(old_content).splitlines()
    new_lines = html2text.html2text(new_content).splitlines()
    diff = difflib.HtmlDiff().make_file(old_lines, new_lines, fromdesc='Before', todesc='After')

    with open(DIFF_HTML, "w", encoding='utf-8') as f:
        f.write(diff)

    return DIFF_HTML

# ---- STEP 3: Convert diff to PDF ----
def generate_pdf(html_path):
    pdfkit.from_file(html_path, DIFF_PDF)
    return DIFF_PDF

# ---- STEP 4: Send email with PDF ----
def send_email(pdf_path):
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = EMAIL_SUBJECT
    msg.set_content("Changes were detected on the monitored webpage. Please find the attached diff report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

# ---- STEP 4.1: Send email with PDF ----
def send_email_with_attachment(sender, password, recipient, subject, body, attachment_path):
    # Create the email message
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach file
    if attachment_path:
        file_name = os.path.basename(attachment_path)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type, mime_subtype = mime_type.split('/')

        with open(attachment_path, 'rb') as file:
            msg.add_attachment(
                file.read(),
                maintype=mime_type,
                subtype=mime_subtype,
                filename=file_name
            )

    # Connect to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
        print("Email sent successfully.")

# ---- MAIN ----
if __name__ == "__main__":
    try:
        current_html = fetch_page_local()
        diff_file = detect_change(current_html)
        if diff_file:
            print("Change detected. Generating report...")
            # pdf_file = generate_pdf(diff_file)
            # html_to_pdf(DIFF_HTML,DIFF_PDF)
            # convert_html_to_pdf(DIFF_HTML,DIFF_PDF)
            render_html_to_pdf(DIFF_HTML,DIFF_PDF)
            # send_email(DIFF_PDF)
            send_email_with_attachment(
            sender="harshapaul@gmail.com",
            password="ngws nhzp yrjz mecd",  # Use app password if 2FA is enabled
            recipient="harshapaul@gmail.com",
            subject="Webpage Change Detected",
            body="Please see the attached file.",
            attachment_path=DIFF_PDF
            )
            print("Email sent with diff PDF.")
        else:
            print("No change detected.")
    except Exception as e:
        print(f"Error: {e}")
