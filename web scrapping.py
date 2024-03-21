import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

def slow_scroll(driver):
    # Simulate scrolling by pressing the down arrow key
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)  # Adjust scrolling speed if needed

def click_load_more_button(driver):
    retries = 3
    for _ in range(retries):
        try:
            load_more_button = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".load-more-btn")))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(15)
            return True
        except TimeoutException:
            print("Timeout waiting for the button to be clickable.")
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue
    print("Failed to click Load More button after retries.")
    return False

# Set to store unique titles
unique_titles = set()

url = " "
chrome_driver_path = r" "
service = Service(chrome_driver_path)
service.start()
driver = webdriver.Remote(service.service_url)
driver.get(url)

driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
time.sleep(2)

titles_to_collect = 4662

while len(unique_titles) < titles_to_collect:
    slow_scroll(driver)
    if not click_load_more_button(driver):
        print("No more 'Load More Colleges' button available. Exiting loop.")
        break
    
    extracted_titles = []
    try:
        extracted_titles = [h3_tag.text.strip() for h3_tag in driver.find_elements(By.CSS_SELECTOR, "h3.f7cc")]
    except NoSuchElementException:
        print("No titles found on the page.")
        break
    
    for title in extracted_titles:
        unique_titles.add(title)

    if len(unique_titles) == titles_to_collect:
       print(f"Titles collected: {len(unique_titles)}")


# Convert set of unique titles to a DataFrame
df = pd.DataFrame(unique_titles, columns=['College Titles'])

# Save DataFrame to Excel file
excel_file_path = r" "
df.to_excel(excel_file_path, index=False)

print("Data saved to Excel file successfully.")
driver.quit()
