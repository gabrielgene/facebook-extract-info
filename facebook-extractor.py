#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import re
import time


def remove_cta(browser):
    element = browser.find_element_by_css_selector(
        "#pagelet_growth_expanding_cta > div")
    browser.execute_script("""
        var element = arguments[0];
        if (element) element.parentNode.removeChild(element);
        """, element)


def get_pictures_from_gallery(browser, profile_name):
    print("Pictures from gallery...")
    img_el = browser.find_element_by_css_selector("#content_container img")
    remove_cta(browser)
    hover = ActionChains(browser).move_to_element(img_el)
    hover.perform()
    time.sleep(1)
    img_el.click()
    time.sleep(1)
    remove_cta(browser)
    pictures = browser.find_elements_by_css_selector(
        "#content_container a img")
    for idx, picture in enumerate(pictures):
        if idx >= 30:
            break
        print("Getting img: {}".format(idx))
        picture.click()
        time.sleep(3)
        try:
            img_url = browser.find_element_by_css_selector(
                ".spotlight").get_attribute("src")
            save_img(img_url, str(idx), "./{}".format(profile_name))
            browser.find_element_by_css_selector("._xlt").click()
            time.sleep(1)
        except Exception:
            print("Erro on download picture")


def get_profile_picture(browser):
    print("Profile image...")
    profile_image = browser.find_element_by_css_selector(
        "#entity_sidebar img").get_attribute("src")
    return profile_image


def save_img(img_url, img_name, path):
    img_data = requests.get(img_url).content
    with open("{}/{}.jpg".format(path, img_name), 'wb') as handler:
        handler.write(img_data)


def get_about_info(browser, profile_url, profile_name):
    print("Getting about page...")
    path = "./{}".format(profile_name)
    main_url = "https://www.facebook.com/pg/bandadexysoficial/about/"
    browser.get("{}about".format(profile_url))

    print("Getting capa...")
    try:
        cover_url = browser.find_element_by_css_selector(
            "#pagelet_page_cover img").get_attribute("src")
        save_img(cover_url, 'cover', path)
    except Exception:
        print("Profile dont have img cover")

    print("Getting about data...")
    data = browser.find_element_by_css_selector("#content_container").text
    with open("{}/info.txt".format(path), 'w+') as handler:
        handler.write(data)
    print(data)


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("no-sandbox")

print("Instance browser")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

profiles = [
    # "https://www.facebook.com/djpetethazouk/",
    "https://www.facebook.com/KURADJ/",
    # "https://www.facebook.com/djvascoamaral/"
]

for p in profiles:
    start_time = time.time()
    profile_name = re.search("\.com\/(\w+)\/", p).group(1)
    print("Getting profile: {}".format(p))
    print("Getting gallery")
    browser.get("{}photos".format(p))
    time.sleep(1)
    if not os.path.exists(profile_name):
        os.makedirs(profile_name)
    profile_image_url = get_profile_picture(browser)
    save_img(profile_image_url, 'profile', "./{}".format(profile_name))
    get_pictures_from_gallery(browser, profile_name)
    get_about_info(browser, p, profile_name)
    print("--- %s seconds ---" % (time.time() - start_time))
