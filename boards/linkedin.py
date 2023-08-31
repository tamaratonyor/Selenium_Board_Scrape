from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
)


class LinkedIn:
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
            for x in range(0, 45):
                df_list.append(self.create_page_df(driver))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("Scrolled further Down")
                try:
                    WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "button[data-tracking-control-name=infinite-scroller_show-more]",
                            )
                        )
                    ).click()
                except TimeoutException:
                    print("Still Scrolling")

        df = pd.concat(df_list, ignore_index=True).drop_duplicates(
            subset=["Job_Title", "Company"], keep="first"
        )
        driver.quit()
        return df

    def create_page_df(self, driver):
        title_elements = driver.find_elements(
            By.CSS_SELECTOR,
            "a[data-tracking-control-name=public_jobs_jserp-result_search-card]",
        )
        company_elements = driver.find_elements(
            By.CSS_SELECTOR, "h4.base-search-card__subtitle"
        )
        location_elements = driver.find_elements(
            By.CSS_SELECTOR, "span.job-search-card__location"
        )
        urls = []
        titles = []
        companies = []
        locations = []
        for element in title_elements:
            urls.append(element.get_attribute("href"))
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
