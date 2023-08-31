from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SimplyHired:
    def scrape(self, search_parameters, url):
        df_list = []
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        for parameter in search_parameters:
            driver.get(url.format(parameter))
            while True:
                df_list.append(self.create_page_df(driver))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "li.next-pagination")
                        )
                    ).click()
                    print("Navigated to Next Page")
                except TimeoutException:
                    print("Last Page Reached")
                    break
        df = pd.concat(df_list, ignore_index=True).drop_duplicates(
            subset=["Job_Title", "Company"], keep="first"
        )
        return df

    def create_page_df(self, driver):
        title_elements = driver.find_elements(
            By.XPATH, "//h3[@class = 'jobposting-title']"
        )
        company_elements = driver.find_elements(
            By.XPATH, "//span[@class = 'JobPosting-labelWithIcon jobposting-company']"
        )
        location_elements = driver.find_elements(
            By.XPATH, "//span[@class = 'jobposting-location']"
        )
        id_elements = driver.find_elements(By.XPATH, "//h3/a")
        urls = []
        titles = []
        companies = []
        locations = []
        for element in id_elements:
            urls.append(
                "https://www.simplyhired.ca" + element.get_attribute("data-mdref")
            )
        for element in title_elements:
            titles.append(element.text)
        for element in company_elements:
            companies.append(element.text)
        for element in location_elements:
            locations.append(element.text)

        if len(titles) == len(companies) == len(locations) == len(urls):
            df = pd.DataFrame(
                {
                    "Job_Title": titles,
                    "Company": companies,
                    "Location": locations,
                    "URL": urls,
                    "Date_Pulled": date.today(),
                }
            )
        return df
