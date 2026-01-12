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




def big_boy_pdf():
    #name the file the course name + "combined"
    #if the file exists here, delete it first before merging.
    #AND save combined one level up (not in individual)
    non_ind_folder_path = f"output/{folder}"
    merger = PdfWriter()
    files = os.listdir(folder_path)
    for pdf in files:
        full_path = os.path.join(folder_path, pdf)
        if os.path.isfile(full_path):
            print(f"appending {full_path}")
            merger.append(full_path)
    with open(f"{non_ind_folder_path}/combined.pdf", "wb") as fout:
        merger.write(fout)

    merger.close()


def sanitize(str):
    """Accepts a string and removes any non-standard characters for file systems"""
    pattern = r'[^a-zA-Z0-9]'
    str = re.sub(pattern, ' ', driver.title)
    return str

#seeee
# 1. Initialize the WebDriver (e.g., Chrome)
# Ensure the path to your chromedriver executable is correct
driver = webdriver.Chrome()

try:
    # 2. Navigate to a website
    driver.get("https://ects-cmp.com/course_content/"
               "")
    # driver.get("https://ects-cmp.com/course_content/wp-login.php?redirect_to=https%3A%2F%2Fects-cmp.com%2Fcourse_content%2F")
    print(f"Page title: {driver.title}")

    # Example using By.ID
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".wpo365-mssignin-button"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type=email]"))
    )
    element.send_keys("cmp_dalysychenko@ects.org")

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#idSIButton9"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type=password]"))
    )
    element.send_keys("Ects0719")

    # input()
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#idSIButton9"))
    )
    element.click()
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#idBtn_Back"))
    )
    element.click()
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".menu-item")))
    # wait = WebDriverWait(driver, 5)
    menu_items = driver.find_elements(By.CSS_SELECTOR, ".menu-item")
    sub_menu_items = driver.find_elements(
        By.CSS_SELECTOR, ".sub-menu .menu-item")
    # for item in menu_items:
    #     print(item.text)

    for item in sub_menu_items:
        print(item.text)

    links = driver.find_elements(By.CSS_SELECTOR, ".menu-item a")
    elements = [{"url": l.get_attribute("href"), "text": l.get_attribute(
        "text")} for l in links if l.get_attribute("href")]

    for idx, elem in enumerate(elements):
        # driver.get(elem["url"])
        print(f"{idx}:  {elem["text"]} : {elem["url"]}")

    choice = input("Enter the index of the page to process: ")
    driver.get(elements[int(choice)]["url"])
    folder = elements[int(choice)]["text"]

    # program grabs all links on selected page. Opens them, saves the page to pdf.
    # stores all pdfs in a folder (maintaining order)
    # after all pdfs are processed, combines them together in the appropriate order.

    content_links = driver.find_elements(
        By.CSS_SELECTOR, ".entry-content a[data-type=post]")

    urls_to_visit = [url.get_attribute("href") for url in content_links if url.get_attribute(
        "href") and "http" in url.get_attribute("href")]

    # for link in content_links:
    #     url = link.get_attribute("href")
    #     if url and "http" in url:  # Ensure it's a valid link
    #         urls_to_visit.append(url)

    print(f"Found {len(urls_to_visit)} links to process...")
    folder_path = f"output/{folder}/individual"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print(folder_path)
    for index, target_url in enumerate(urls_to_visit):
        print(f"Visiting ({index + 1}/{len(urls_to_visit)}): {target_url}")

        # Navigate to the link
        driver.get(target_url)

        # --- YOUR PROCESSING CODE GOES HERE ---
        # Example: wait for content to load
        time.sleep(2)
        # Example: print page title
        print(f"  Loaded: {driver.title}")
        save_page_as_pdf(
            driver, target_url, f"{folder_path}/{str(index).rjust(3, "0")}_{sanitize(driver.title)}.pdf")

        # ---------------------------------------

        # Since we are using a list of URLs, we don't need to 'go back'
        # unless the site structure requires a specific flow.

    big_boy_pdf()

    hold = input("Press enter to close ")


finally:
    # 7. Close the browser
    driver.quit()
    print("Browser closed.")


# ToDo:
# Sanitize
# combine pdfs - put in folder - output/coursename/combined
# output/coursename/individual
# output/coursename/coursename.pdf
