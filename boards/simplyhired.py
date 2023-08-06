from selenium import webdriver

class SimplyHired:
    def scrape(search_parameters, url):
        driver = webdriver.Chrome()
        driver.get(url)
        value = driver.find_elements_by_class_name('')
        text = value.find_element_by_xpath('.') # include . if reading from an element as we do here with value
