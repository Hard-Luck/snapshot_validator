import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from wallets_20000 import ADDRESSES

# Initialize the webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


# Chainz URL
BASE_URL = "https://chainz.cryptoid.info/phr/address.dws?"


def download_csv(address: str) -> None:
    """Download CSV file of all transactions for a given wallet"""

    # Open page of address
    driver.get(f"{BASE_URL}{address}")
    # Find download link and click into it
    download_link = driver.find_element(By.ID, "download-csv")
    download_link.click()
    time.sleep(5)


def main() -> None:
    """Query ever address imported from Wallets and download the csv transactions"""
    for address in ADDRESSES:
        download_csv(address)
        time.sleep(10)


if __name__ == "__main__":
    main()
