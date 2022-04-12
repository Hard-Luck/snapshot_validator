import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
BASE_URL = "https://chainz.cryptoid.info/phr/address.dws?"

# Block Heights
Snapshots = [
    "1817125",
    "1856572",
    "1896008",
    "1935435",
    "1971468",
    "1999951",
]


def get_balance(address: str, snapshot: str) -> int:

    driver.get(f"{BASE_URL}{address}")
    # Find filter search box and click into it
    filter_box = driver.find_element(By.ID, "view-fts")
    filter_box.click()

    # Type the block into the search
    filter_box.send_keys(snapshot)

    # make wait so page can load
    time.sleep(2)
    # Get the block as a table and format it extracting the balance
    table = driver.find_element(By.ID, "transactions").text.split()

    balance = float("".join(table[-2] + table[-1]).replace(",", ""))
    return balance


balances = []
for snapshot in Snapshots:
    try:
        values = get_balance("PXYtJUh8mxDYARjkk4Kctix9H7ewDuGmNd.htm", snapshot)
    except:
        values = 0
    balances.append(values)
print(balances)
