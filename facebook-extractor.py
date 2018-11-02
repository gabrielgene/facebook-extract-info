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
    try:
        element = browser.find_element_by_css_selector(
            "#pagelet_growth_expanding_cta > div")
        browser.execute_script("""
            var element = arguments[0];
            if (element) element.parentNode.removeChild(element);
            """, element)
    except Exception:
        print("Dont find CTA")


def save_img(img_url, img_name, path):
    img_data = requests.get(img_url).content
    with open("profiles/{}/{}.jpg".format(path, img_name), 'wb') as handler:
        handler.write(img_data)


def get_about_info(browser, profile_url, profile_name):
    print("Getting about page...")
    path = "./{}".format(profile_name)
    main_url = "https://www.facebook.com/pg/bandadexysoficial/about/"
    browser.get("{}about".format(profile_url))
    print("Getting about data...")
    data = browser.find_element_by_css_selector("#content_container").text
    with open("profiles/{}/info.txt".format(path), 'w+') as handler:
        handler.write(data)


def get_all_galleries(browser):
    print("Getting all galleries")
    all_galleries_element = browser.find_element_by_css_selector(
        "div._ohf.rfloat > a")
    link = all_galleries_element.get_attribute("href")
    browser.get(link)
    time.sleep(1)
    browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    remove_cta(browser)


def get_gallery(gallery_name, browser, profile_name):
    print("Getting gallery {}".format(gallery_name))
    browser.get("{}photos".format(p))
    time.sleep(1)
    remove_cta(browser)
    get_all_galleries(browser)
    list_of_galleries = browser.find_elements_by_css_selector(
        "#u_0_l > div > div:nth-child(2) > div")
    limit = 1
    folder_type = ''
    print(len(list_of_galleries))
    for gallery in list_of_galleries:
        hover = ActionChains(browser).move_to_element(gallery)
        hover.perform()
        found = re.search(gallery_name, gallery.text)
        if found:
            hover = ActionChains(browser).move_to_element(gallery)
            hover.perform()
            time.sleep(1)
            try:
                gallery.click()
                time.sleep(1)
                if gallery_name == "Fotos da capa":
                    limit = 2
                    folder_type = 'cover'
                if gallery_name == "Fotos do perfil":
                    limit = 2
                    folder_type = 'profile'
                if gallery_name == "Fotos da linha do tempo":
                    limit = 2
                get_pictures_from_gallery(
                    browser, limit, profile_name, folder_type)
                break
            except Exception:
                print("Erro on click in gallery")


def get_pictures_from_gallery(browser, limit, profile_name, folder_type):
    print("Limit {}".format(limit))
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

print("Create browser")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

profiles = [
    # "https://www.facebook.com/djpetethazouk/",
    "https://www.facebook.com/KURADJ/",
    "https://www.facebook.com/djvascoamaral/",
    "https://www.facebook.com/dj.XDirty/",
    "https://www.facebook.com/thedjalext/",
    "https://www.facebook.com/djpedro.pt/",
    "https://www.facebook.com/djkaisert/",
    "https://www.facebook.com/Dj-Thrasher-86162038072/",
    "https://www.facebook.com/analodjicapt/",
    "https://www.facebook.com/paulsoir/",
    "https://www.facebook.com/HugoJardimDJ/",
    "https://www.facebook.com/DjAndreFortunato/",
    "https://www.facebook.com/philkl4nkmusic/",
    "https://www.facebook.com/djtiagoaz/",
    "https://www.facebook.com/djmiguelrendeiro/",
    "https://www.facebook.com/pedrotabuada/",
    "https://www.facebook.com/jiggysounds/",
    "https://www.facebook.com/ruivargasdj/",
    "https://www.facebook.com/gimba.oficial/",
    "https://www.facebook.com/EnaPa2000/",
    "https://www.facebook.com/Miguel.Angelo.Delfins/",
    "https://www.facebook.com/PauloGonzoMusic/",
    "https://www.facebook.com/pedrotochas/",
    "https://www.facebook.com/WilsonPOficial/",
    "https://www.facebook.com/djstikup1/",
    "https://www.facebook.com/DjGabyOfficial/",
    "https://www.facebook.com/kataleya/",
    "https://www.facebook.com/pupilosdokuduro/",
    "https://www.facebook.com/GeneralSemMedo/",
    "https://www.facebook.com/edduoffcial/"
]

galleries = ["Fotos da capa", "Fotos do perfil", "Fotos da linha do tempo"]

for p in profiles:
    start_time = time.time()

    profile_name = re.search("\.com\/(\w+.+)\/", p).group(1)
    print("Getting profile: {}".format(p))
    if not os.path.exists("profiles/{}".format(profile_name)):
        os.makedirs("profiles/{}".format(profile_name))

    for gallery_name in galleries:
        print("Getting {}".format(gallery_name))
        get_gallery(gallery_name, browser, profile_name)
    get_about_info(browser, p, profile_name)
    print("--- %s seconds ---" % (time.time() - start_time))
browser.close()
