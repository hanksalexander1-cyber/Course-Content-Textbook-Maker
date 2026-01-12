from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from printerdemo import save_page_as_pdf
from pypdf import PdfWriter
import re
import time
import os
from dotenv import load_dotenv

load_dotenv()
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def pdf_combiner():
    """name the file the course name + "combined"
    if the file exists here, delete it first before merging.
    save combined one level up (not in individual)"""
    merger = PdfWriter()
    files = os.listdir(folder_path)
    for pdf in files:
        full_path = os.path.join(folder_path, pdf)
        if os.path.isfile(full_path):
            print(f"appending {full_path}")
            merger.append(full_path)
    with open(f"{folder_path}/combined.pdf", "wb") as fout:
        merger.write(fout)

    merger.close()


def sanitize(str):
    """Accepts a string and removes any non-standard characters for file systems"""
    pattern = r'[^a-zA-Z0-9]'
    str = re.sub(pattern, ' ', driver.title)
    return str


def list_options(urls_to_visit):
    for index, target_url in enumerate(urls_to_visit):
        print(f"Visiting ({index + 1}/{len(urls_to_visit)}): {target_url}")

        # Navigate to the link
        driver.get(target_url)

        time.sleep(2)
        #wait for content to load
        print(f"  Loaded: {driver.title}")
        save_page_as_pdf(driver, target_url, f"{folder_path}/individual/{str(index).rjust(3, "0")}_{sanitize(driver.title)}.pdf")

        # Since we are using a list of URLs, we don't need to 'go back'
        # unless the site structure requires a specific flow.

def wait_and_click_button(button_class, login_class, login_creds):
    """waits until the url loads or 10 seconds pass by before clicking on a button using css.selecter and its class in the button_class parameter"""
    if button_class != "":
        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_class))
        )
        element.click()
    if login_class != "":
        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, login_class))
        )
        element.send_keys(login_creds)

def find_elements(classname):
    """finds elements in the selected area by using css_selecter and the classnames"""
    items = driver.find_elements(By.CSS_SELECTOR, classname)

try:
    """program grabs all links on selected page. Opens them, saves the page to pdf.
    stores all pdfs in a folder (maintaining order)
    after all pdfs are processed, combines them together in the appropriate order."""


    # 2. Navigate to a website
    driver.get("https://ects-cmp.com/course_content/""")

    print(f"Page title: {driver.title}")

    wait_and_click_button(".wpo365-mssignin-button", "", "")

    wait_and_click_button("","input[type=email]", os.getenv("USER_EMAIL"))

    wait_and_click_button("#idSIButton9", "", "")

    wait_and_click_button("", "input[type=password]", os.getenv("USER_PASS"))

    wait_and_click_button("#idSIButton9", "", "")

    time.sleep(2)

    wait_and_click_button("#idBtn_Back", "", "")



    elements = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".menu-item")))
    
    menu_items = find_elements(".menu-items")
    sub_menu_items = find_elements(".sub-menu .menu-item")

    for item in sub_menu_items:
        print(item.text)

    links = driver.find_elements(By.CSS_SELECTOR, ".menu-item a")
    elements = [{"url": l.get_attribute("href"), "text": l.get_attribute(
        "text")} for l in links if l.get_attribute("href")]

    for idx, elem in enumerate(elements):
        print(f"{idx}:  {elem["text"]} : {elem["url"]}")

    choice = input("Enter the index of the page to process: ")
    driver.get(elements[int(choice)]["url"])
    folder = elements[int(choice)]["text"]
    folder_path = f"output/{folder}"
    

    content_links = driver.find_elements(
        By.CSS_SELECTOR, ".entry-content a[data-type=post]")

    urls_to_visit = [url.get_attribute("href") for url in content_links if url.get_attribute(
        "href") and "http" in url.get_attribute("href")]

    #tells you how many urls the code found
    print(f"Found {len(urls_to_visit)} links to process...")

    if not os.path.exists(f"{folder_path}/individual"):
        os.makedirs(f"{folder_path}/individual")


    list_options()

    pdf_combiner()

    hold = input("Press enter to close ")


finally:
    # 7. Close the browser
    driver.quit()
    print("Browser closed.")

