import json
import logging
import os
import re
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def close_all_except_first():
    """
    Close all tabs except the first tab.
    """

    for handle in browser.window_handles[1:]:
        browser.switch_to.window(handle)
        browser.close()
    browser.switch_to.window(browser.window_handles[0])


def close_all_except_last():
    """
    Close all tabs except the last tab.
    """

    for handle in browser.window_handles[:-1]:
        browser.switch_to.window(handle)
        browser.close()
    browser.switch_to.window(browser.window_handles[-1])


def close_all():
    """
    Close all tabs
    """

    for handle in browser.window_handles:
        browser.switch_to.window(handle)
        browser.close()


def process_intercelestial():
    """
    Process Intercelestial.
    """

    if not ("intercelestial" in browser.current_url or "linegee" in browser.current_url):
        return

    wait_elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "soralink-human-verif-main")))
    while "display: none" in wait_elem.get_attribute("style"):
        time.sleep(1)
    wait_elem.click()

    wait_elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "generater")))
    while "display: none" in wait_elem.find_element(By.XPATH, "..").get_attribute("style"):
        time.sleep(1)
    wait_elem.click()

    wait_elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "showlink")))
    while "display: none" in wait_elem.get_attribute("style"):
        time.sleep(1)
    wait_elem.click()


def process_spacetica():
    """
    Process Spacetica.

    Returns:
        str: Final URL.
    """

    if "spacetica" not in browser.current_url:
        return

    for btn_elem in browser.find_elements(By.CLASS_NAME, "btn"):
        if btn_elem.text == "Continue":
            return btn_elem.get_attribute("href") or btn_elem.find_element(By.XPATH, "..").get_attribute("href")


def get_download_titles(download_page_url, counter):
    # Switch to the newly opened window
    browser.get(download_page_url)

    # Make all 'pane' elements visible && Add ID
    for index, pane_elem in enumerate(browser.find_elements(By.CLASS_NAME, "pane")):
        browser.execute_script(f"arguments[0].id = 'pane_{index}';", pane_elem)
        browser.execute_script("arguments[0].style.display = 'block';", pane_elem)

    # Add span tags to innerText
    for box_elem in browser.find_elements(By.CLASS_NAME, "box-inner-block"):
        browser.execute_script("""
        var element = arguments[0];
        var childNodes = element.childNodes;
        for(var i=0; i<childNodes.length; i++) {
            var node = childNodes[i];
            if (node.nodeType === 3 && node.nodeValue.trim() !== "") {
                var span = document.createElement('span');
                span.textContent = node.nodeValue;
                element.insertBefore(span, node);
                element.removeChild(node);
            }
        }
        """, box_elem)

        # Replace all <b> tags with <span> tags using JavaScript
        browser.execute_script("""
            var elements = document.getElementsByTagName('b');
            for (var i = 0; i < elements.length; i++) {
                var span = document.createElement('span');
                span.innerHTML = elements[i].innerHTML;
                elements[i].parentNode.replaceChild(span, elements[i]);
            }
        """, box_elem)

        # Merge consecutive <span> elements
        browser.execute_script("arguments[0].innerHTML = arguments[0].innerHTML.replaceAll('</span><span>',' ')", box_elem)

    # Find all download button elements
    btn_elems = browser.find_elements(By.CLASS_NAME, "shortc-button")

    # Select the button to click based on the counter
    btn_elem = btn_elems[counter]

    # Get Download Pane Text
    pane_elem_id = int(btn_elem.find_element(By.XPATH, "../../..").get_attribute("id").replace("pane_", ""))
    pane_text = browser.find_element(By.CLASS_NAME, "tabs-nav").find_elements(By.TAG_NAME, "li")[pane_elem_id].text
    pane_text = pane_text.replace("|", "-").strip()

    # Find Box Title
    box_title = btn_elem.find_element(By.XPATH, "..").find_elements(By.XPATH, "*")[1].text
    box_title = box_title.replace("|", "-").strip()
    box_title = box_title.replace(f"{pane_text} – ", "").strip()

    # Get Download Format Text
    download_format = btn_elem.find_element(By.XPATH, "preceding::span[1]").text
    download_format = download_format.replace("|", "-").strip()

    # Navigate to the download page
    browser.get(download_page_url)

    return pane_text, box_title, download_format


def click_download_btn(download_page_url, btn):
    """
    Simulates a click on a download button, processes Intercelestial and Spacetica pages, and navigates to a download page.

    Args:
    - download_page_url (str): The URL of the download page to navigate to.
    - btn (WebElement): The WebElement object representing the download button to click.

    Returns:
    - str: The final URL after processing Spacetica.
    """

    # Click Download button
    btn.click()

    # Process Intercelestial
    close_all_except_first()
    process_intercelestial()

    # Process Spacetica
    close_all_except_last()
    final_url = process_spacetica()

    # Navigate to the download page
    browser.get(download_page_url)

    return final_url


def single(download_page_url, counter=0, json_data=None):
    """
    Function to iterate through download buttons on a page and click them.

    Args:
        download_page_url (str): The URL of the page containing download buttons.
        counter (int): The index of the button to start from.
        json_data (dict): The json data of the download buttons
    """

    # Find all download button elements
    btn_elems = browser.find_elements(By.CLASS_NAME, "shortc-button")
    btn_elems_length = len(btn_elems)

    # Select the button to click based on the counter
    btn_elem = btn_elems[counter]

    # Find the parent element of the button and extract box title and type title
    box_title = btn_elem.find_element(By.XPATH, "preceding::b[1]").text

    # Log box title and type title
    logging.info(f"{counter + 1}/{btn_elems_length} ({int((counter + 1) / btn_elems_length * 100)} %) | {box_title} - {btn_elem.text}")

    # Click the download button
    final_url = click_download_btn(download_page_url, btn_elem)
    logging.info(f"{final_url}")
    logger.info("--------------------")

    # Add to json data
    json_data = {} if json_data is None else json_data
    json_data[box_title] = json_data.get(box_title, []) + [final_url]

    # If there are more buttons to click, recursively call the function with the next counter
    if counter < btn_elems_length - 1:
        single(download_page_url, counter + 1, json_data)

    return json_data


def multi(download_page_url, counter=0, json_data=None):
    """
    Function to iterate through download buttons on a page and click them.

    Args:
        download_page_url (str): The URL of the page containing download buttons.
        counter (int): The index of the button to start from.
        json_data (dict): The json data of the download buttons
    """

    # Get Download Titles
    pane_text, box_title, download_format = get_download_titles(download_page_url, counter)

    # Find all download button elements
    btn_elems = browser.find_elements(By.CLASS_NAME, "shortc-button")
    btn_elems_length = len(btn_elems)

    # Select the button to click based on the counter
    btn_elem = btn_elems[counter]

    # Log box title and type title
    logging.info(f"{counter + 1}/{btn_elems_length} ({int((counter + 1) / btn_elems_length * 100)} %) | {pane_text} | {box_title} | {download_format} - {btn_elem.text}")

    # Click the download button
    final_url = click_download_btn(download_page_url, btn_elem)
    logging.info(f"{final_url}")
    logger.info("--------------------")

    # Add to json data
    json_data = {} if json_data is None else json_data
    if pane_text not in json_data:
        json_data[pane_text] = {}
    if box_title not in json_data[pane_text]:
        json_data[pane_text][box_title] = {}
    json_data[pane_text][box_title][download_format] = json_data[pane_text][box_title].get(download_format, []) + [final_url]

    # If there are more buttons to click, recursively call the function with the next counter
    if counter < btn_elems_length - 1:
        multi(download_page_url, counter + 1, json_data)

    return json_data


def main():
    """
    This function takes a URL as an argument, visits the specified download page using Selenium,
    detects the mode of the page (Single or Multi), crawls the page accordingly, and saves the
    crawled data to a JSON file.

    Usage:
        python3 script.py <download_page_url>
    """

    # Visit Download Page
    # download_page_url = sys.argv[1]
    download_page_url = "https://pahe.ink/shogun-season-1/"
    # download_page_url = "https://pahe.ink/hawaii-five-0-season-8-10-complete-bluray-720p/"
    logger.info(f"URL - {download_page_url}")
    browser.get(download_page_url)
    page_title = browser.title
    logger.info(f"Title - {page_title}")

    # Detect mode
    mode = "Multi" if browser.find_elements(By.CLASS_NAME, "tabs-nav") else "Single"
    logger.info(f"Detected {mode} Mode")
    logger.info("--------------------")

    # Crawl
    json_data = multi(download_page_url) if mode == "Multi" else single(download_page_url)

    # Save json_data to file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{re.sub(r'[^a-zA-Z0-9]', '', page_title)}.json"), "w") as out_file:
        json.dump(json_data, out_file, indent=4)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace('.py', '.log')}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    # Create Selenium
    logger.info("Launch Browser")
    Options = Options()
    Options.add_argument("-headless")
    Options.binary_location = "/Applications/Brave Browser.app"
    browser = webdriver.Chrome(options=Options)
    logger.info("--------------------")

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
    finally:
        browser.quit()
        logger.info("Close")
        logger.info("End")
