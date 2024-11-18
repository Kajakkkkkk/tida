from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/cookieclicker/")

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))


try:
    consent_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-dialog-container .fc-button")))
    consent_button.click()
except (NoSuchElementException, ElementClickInterceptedException):
    pass

try:
    language_selection = wait.until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
    language_selection.click()
except (NoSuchElementException, ElementClickInterceptedException):
    pass

Big_cookie = wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))

# Pobieranie budynkow
def get_available_buildings():
    return driver.find_elements(By.CSS_SELECTOR, "#products .product.unlocked.enabled")

# Pobieranie ulepszen
def get_available_upgrades():
    return driver.find_elements(By.CSS_SELECTOR, "#upgrades .crate.upgrade.enabled")


last_check_time = time.time()

while True:
    # Klikanie w ciastko
    try:
        Big_cookie.click()
    except StaleElementReferenceException:
        Big_cookie = wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))

    # Sprawdzanie ulepszen i budynkww
    current_time = time.time()
    if current_time - last_check_time > 5:
        last_check_time = current_time

        # Kupowanie dostępnych ulepszen
        upgrades = get_available_upgrades()
        for upgrade in upgrades:
            try:
                upgrade.click()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                continue

        # Kupowanie dostępnych budynkow
        buildings = get_available_buildings()
        for building in reversed(buildings):
            try:
                building.click()
                break
            except (ElementClickInterceptedException, StaleElementReferenceException):
                continue
