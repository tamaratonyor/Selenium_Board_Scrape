from selenium import webdriver
import pandas as pd


class Monster:
    def scrape(search_parameters, url):
        for parameter in search_parameters:
            driver = webdriver.Chrome()
            driver.get(url.format(parameter))
            value = driver.find_elements_by_class_name("")
            text = value.find_element_by_xpath(
                "."
            )  # include . if reading from an element as we do here with value
