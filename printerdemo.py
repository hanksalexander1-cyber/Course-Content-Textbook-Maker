import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




def save_page_as_pdf(driver, url, output_file_name, waittime = 5):
    """
    <h1>A super awesome method to save a selenium loaded page to pdf</h1>
    <ul>
    <li>driver: a selenium web driver</li>
    <li>url: the page to be captured</li>
    <li>output_file_name: the path (including filename) to the file to be saved</li>
    </ul>
    """
        # Force normal desktop rendering — NO scaling
    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": 1920,
            "height": 1080,
            "deviceScaleFactor": 1,   # <- THIS is 100% zoom
            "mobile": False
        }
    )

    driver.get(url)

    # Allow JS, fonts, images, CSS to fully load
    time.sleep(waittime)

    # Print exactly what Chrome renders, with backgrounds
    pdf = driver.execute_cdp_cmd(
        "Page.printToPDF",
        {
            "printBackground": True,
            "preferCSSPageSize": True,
            "scale": 1,              # <- DO NOT SCALE
            "marginTop": 0.4,
            "marginBottom": 0.4,
            "marginLeft": 0.4,
            "marginRight": 0.4
        }
    )

    with open(output_file_name, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))

    print(f"Saved PDF at true 100% zoom: {output_file_name}")

    return pdf["data"]

 