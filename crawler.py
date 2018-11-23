#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests
import re
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("no-sandbox")

browser = webdriver.Chrome('./chromedriver', options=chrome_options)

main_url = "https://www.casamentos.pt/musica-casamento"

browser.get(main_url)
print("Getting main page...")

directory_title = browser.find_elements_by_css_selector(
    ".directory-filtered .title")

profiles_amount = re.search(
    r"(\d+)\s", directory_title[1].text.strip()).group(1)

print(profiles_amount)

list_items = browser.find_elements_by_css_selector(
    ".directory-list .directory-list-item")

test_items = [list_items[0]]
# test_items = list_items

for idx, item in enumerate(test_items):
    img_amount = item.find_element_by_css_selector(
        ".vendor-slider-content .listing-caption-count")
    for i in range(int(img_amount.text.strip())):
        print(i)
        img = item.find_element_by_css_selector(
            ".vendor-slider-content img")
        img_url = img.get_attribute("src")
        print(img_url)
        img_data = requests.get(img_url).content
        with open(str(i)+'.jpg', 'wb') as handler:
            handler.write(img_data)
        hover = ActionChains(browser).move_to_element(item)
        hover.perform()
        item.find_element_by_css_selector(
            ".directory-list-item .mgall-next").click()
        time.sleep(0.5)

browser.close()

PAGE_LIMIT = 12
