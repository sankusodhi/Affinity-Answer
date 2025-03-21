from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import time
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
url = "https://www.olx.in/items/q-car-cover?isSearchCall=true"
driver.get(url)
time.sleep(5)
for _ in range(3): 
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)
wait = WebDriverWait(driver, 15)
try:
    ads = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@data-aut-id, "itemBox")]')))
except:
    print("No data found. Please check if OLX structure has changed.")
    driver.quit()
    exit()

results = []
for ad in ads:
    try:
        title = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "itemTitle")]').text or "N/A"
        price = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "itemPrice")]').text or "N/A"
        location = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "item-location")]').text or "N/A"
    except Exception as e:
        print(f"Error extracting data: {e}")
        title, price, location = "N/A", "N/A", "N/A"

    results.append([title, price, location])
driver.quit()
if results:
    print(tabulate(results, headers=["Title", "Price", "Location"], tablefmt="grid"))
else:
    print("No data found. Please check if OLX structure has changed.")
