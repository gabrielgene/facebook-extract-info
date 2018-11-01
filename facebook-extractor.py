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
    print("Getting about data...")
    data = browser.find_element_by_css_selector("#content_container").text
    with open("{}/info.txt".format(path), 'w+') as handler:
        handler.write(data)


def get_gallery(gallery_name, browser, profile_name):
    print("Getting  gallery {}".format(gallery_name))
    browser.get("{}photos".format(p))
    time.sleep(1)
    remove_cta(browser)
    list_of_galleries = []
    list1 = browser.find_elements_by_css_selector(
        "#content_container > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div")
    list2 = browser.find_elements_by_css_selector(
        "#content_container > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div ")
    if len(list1) == 4:
        list_of_galleries = list1
    if len(list2) == 4:
        list_of_galleries = list2
    limit = 1
    folder_type = ''
    for gallery in list_of_galleries:
        print("Getting gallery")
        hover = ActionChains(browser).move_to_element(gallery)
        hover.perform()
        found = re.search(gallery_name, gallery.text)
        if found:
            hover = ActionChains(browser).move_to_element(gallery)
            hover.perform()
            time.sleep(1)
            gallery.click()
            time.sleep(1)
            if gallery_name == "Fotos da capa":
                limit = 3
                folder_type = 'cover'
            if gallery_name == "Fotos do perfil":
                limit = 3
                folder_type = 'profile'
            if gallery_name == "Fotos da linha do tempo":
                limit = 3
            get_pictures_from_gallery(
                browser, limit, profile_name, folder_type)
            break


def get_pictures_from_gallery(browser, limit, profile_name, folder_type):
    print("Pictures from gallery... limit {}".format(limit))
    remove_cta(browser)
    time.sleep(1)
    pictures = browser.find_elements_by_css_selector(
        "#content_container a img")
    for idx, picture in enumerate(pictures):
        if idx >= limit:
            break
        print("Getting img: {}".format(idx))
        hover = ActionChains(browser).move_to_element(picture)
        hover.perform()
        picture.click()
        time.sleep(3)
        try:
            img_url = browser.find_element_by_css_selector(
                ".spotlight").get_attribute("src")
            save_img(img_url, "{}_{}{}".format(folder_type, profile_name, str(idx)),
                     "./{}".format(profile_name))
            time.sleep(1)
            browser.find_element_by_css_selector("._xlt").click()
            time.sleep(1)
        except Exception:
            print("Erro on download picture")


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("no-sandbox")

print("Instance browser")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

profiles = [
    "https://www.facebook.com/mariaoficial00/",
    "https://www.facebook.com/KURADJ/",
    "https://www.facebook.com/djpetethazouk/",
    "https://www.facebook.com/djvascoamaral/"
]

galleries = ["Fotos da capa", "Fotos do perfil", "Fotos da linha do tempo"]

for p in profiles:
    start_time = time.time()

    profile_name = re.search("\.com\/(\w+)\/", p).group(1)
    print("Getting profile: {}".format(p))
    if not os.path.exists(profile_name):
        os.makedirs(profile_name)

    for gallery_name in galleries:
        print("Getting {}".format(gallery_name))
        get_gallery(gallery_name, browser, profile_name)
    get_about_info(browser, p, profile_name)
    print("--- %s seconds ---" % (time.time() - start_time))
browser.close()
