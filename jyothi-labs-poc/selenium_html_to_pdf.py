import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def render_html_to_pdf(input_html_path, output_pdf_path):
    # Convert local path to file URI
    file_url = 'file://' + os.path.abspath(input_html_path)

    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # new headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--print-to-pdf-no-header")

    # Ensure background colors and images are rendered
    prefs = {
        "printing.print_preview_sticky_settings.appState": '{"recentDestinations": [{"id": "Save as PDF","origin": "local"}],"selectedDestinationId": "Save as PDF","version": 2}',
        "savefile.default_directory": os.getcwd()
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Launch the driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the HTML file
        driver.get(file_url)

        # Wait for the page to load (you can use WebDriverWait here if needed)
        driver.implicitly_wait(2)

        # Step 1: Get full scrollable width in pixels
        scroll_width = driver.execute_script("return document.body.scrollWidth")

        # Step 2: Convert to inches (assuming 96 pixels = 1 inch)
        paper_width_in_inches = round(scroll_width / 96.0, 2)

        # Use Chrome DevTools Protocol to generate the PDF
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "landscape": False,
            "paperWidth": paper_width_in_inches,   # A4 size in inches 8.27
            "paperHeight": 11.69,
        })

        # Write to output path
        with open(output_pdf_path, 'wb') as f:
            f.write(base64.b64decode(pdf['data']))

        print(f"✅ PDF saved to: {output_pdf_path}")
    finally:
        driver.quit()
