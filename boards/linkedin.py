from selenium import webdriver

class LinkedIn:
    def scrape(url):
        driver = webdriver.Chrome()
        driver.get(url)
        value = driver.find_elements_by_class_name('')
        text = value.find_element_by_xpath('.') # include . if reading from an element as we do here with value

        # RUN headless
        # Add next page function
