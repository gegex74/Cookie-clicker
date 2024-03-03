from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")
store = driver.find_elements(By.CSS_SELECTOR, value="#store div")
items = [item.get_attribute("id") for item in store]

timeout = time.time() + 5
game_duration = time.time() + 60 * 5

game_on = True

while game_on:
    cookie.click()

    if time.time() > timeout:
        store_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices = []

        for price in store_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        upgrades = {}
        for upgrade in range(len(item_prices)):
            upgrades[item_prices[upgrade]] = items[upgrade]

        cookies_bank = driver.find_element(By.ID, value="money").text
        if "," in cookies_bank:
            cookies_bank = cookies_bank.replace(",", "")
        money = int(cookies_bank)

        affordable_upgrades = {}
        for cost, id in upgrades.items():
            if money > cost:
                affordable_upgrades[cost] = id

        highest_affordable_upgrade = max(affordable_upgrades)
        buy_upgrade_id = affordable_upgrades[highest_affordable_upgrade]

        driver.find_element(By.ID, value=buy_upgrade_id).click()

        timeout = time.time() + 5

    if time.time() > game_duration:
        record = driver.find_element(By.ID, value="cps").text
        print(record)
        break
