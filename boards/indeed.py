import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Indeed:
    def scrape(self, driver, search_parameters, url):
        df_list = []
        for parameter in search_parameters:
            driver.get(url.format(parameter))
            while True:
                try:
                    df_list.append(self.create_page_df(driver))
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "a[data-testid=pagination-page-next]")
                        )
                    ).click()
                    print("Navigated to Next Page")
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR, "button[aria-label=close]")
                            )
                        ).click()
                    except TimeoutException:
                        print("No Pop Up")
                except TimeoutException:
                    print("Last Page Reached")
                    break
        df = pd.concat(df_list, ignore_index=True).drop_duplicates(
            subset=["Job_Title", "Company"], keep="first"
        )
        driver.quit()
        return df

    def create_page_df(self, driver):
        value = driver.find_element(By.ID, "jobsearch-JapanPage")
        title_elements = value.find_elements(By.XPATH, ".//span[@title]")
        company_elements = value.find_elements(By.CLASS_NAME, "companyName")
        location_elements = value.find_elements(By.CLASS_NAME, "companyLocation")
        urls = []
        titles = []
        companies = []
        locations = []
        for element in title_elements:
            urls.append(
                "https://ca.indeed.com/viewjob?jk="
                + element.get_attribute("id").replace("jobTitle-", "")
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
