import config
import importlib
from logger import logger
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Initialize options for Selenium
options = Options()
options.add_argument("--log-level=3")
options.add_argument("--disable-cache")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(log_path=os.devnull)
driver = webdriver.Chrome(service=service, options=options)


def send_push_pushbullet(title, body, tokens_list):
    """Send push notification to all configured Pushbullet accounts."""
    for token in tokens_list:
        try:
            requests.post(
                config.PUSHBULLET_URL,
                headers={"Access-Token": token},
                json={"type": "note", "title": title, "body": body},
            )
        except Exception as e:
            logger.error(f"Failed to send Pushbullet notification: {e}")


def send_push_ifttt(title, body, tokens_list):
    """Send push notification to all configured IFTTT accounts."""
    for token in tokens_list:
        try:
            requests.post(
                f"{config.IFTTT_URL}{token}",
                headers={"Content-Type": "application/json"},
                json={"title": title, "body": body},
            )
        except Exception as e:
            logger.error(f"Failed to send IFTTT notification: {e}")


def send_push_to_all(title, body):
    send_push_pushbullet(title, body, config.PUSHBULLET_TOKENS)
    send_push_ifttt(title, body, config.IFTTT_KEYS)


def get_company_names_and_urls():
    """Collect and return a dict mapping company names to their booth URLs."""
    company_url_map = {}
    tiles = driver.find_elements(By.CSS_SELECTOR, "div.rf-tile-wrapper.exhibitor-tile")

    for tile in tiles:
        button = tile.find_element(By.CSS_SELECTOR, "a.exhibitor-tile-view-booth")
        company = button.get_attribute("aria-label").replace("View Booth ", "")
        data_test = tile.get_attribute("data-test")
        exhibitor_id = data_test.split("-")[-1]
        booth_url = f"/exhibitor/{exhibitor_id}"
        company_url_map[company] = booth_url

    logger.debug(f"Found {len(company_url_map)} companies in the catalog.")

    return company_url_map


def check_slots_available(company):
    """Check if the Request Meeting button is enabled."""
    try:
        button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[data-analytics-name='request-meeting']")
            )
        )
        if button.get_attribute("disabled") is None:
            logger.critical(f"{company} button is ENABLED!")
            send_push_to_all("GHC 1:1 Alert!", f"{company} slot available.")
    except Exception:
        logger.debug(f"Request Meeting Button doesn't exist for {company}.")


def get_monitored_companies_dict():
    companies = get_company_names_and_urls()
    if config.MONITOR_ALL_EXCEPT_BLACKLIST:
        logger.debug("Monitoring all companies, except the ones in ALERT_BLACKLIST.")
        companies = companies = {
            k: v for k, v in companies.items() if k not in config.ALERT_BLACKLIST
        }
    else:
        logger.debug("Monitoring the companies in ALERT_WHITELIST only.")
        companies = companies = {
            k: v for k, v in companies.items() if k in config.ALERT_WHITELIST}
        }
    return companies


# --- Main Execution ---
driver.get(config.CATALOG_URL)
logger.info("Please log in manually in the browser window and press ENTER here.. ")
input()
time.sleep(3)

user_requested_exit = False

try:
    while True:
        companies = get_monitored_companies_dict()
        logger.debug(f"\nChecking slots for {len(companies)} companies:")
        logger.debug(", ".join(companies))
        for company_name in companies:
            driver.get(config.CATALOG_URL.rstrip("/") + companies[company_name])
            check_slots_available(company_name)
        logger.debug(
            f"Checked all companies. Sleeping for {config.SCRIPT_SLEEP_DURATION} seconds."
        )
        logger.info("Press CTRL+C to exit.")
        driver.switch_to.new_window("tab")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(config.CATALOG_URL)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
        time.sleep(config.SCRIPT_SLEEP_DURATION)
        logger.debug("Reloading config.")
        importlib.reload(config)
except KeyboardInterrupt:
    user_requested_exit = True
    logger.debug("User requested exit.")
finally:
    if driver:
        driver.quit()
        logger.debug("Browser closed.")
        if not user_requested_exit:
            logger.error("Crash detected!")
            send_push_pushbullet(
                "SCRIPT CRASHED",
                "Restart script immediately.",
                config.PUSHBULLET_TESTING_AND_ERROR_TOKENS,
            )
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
