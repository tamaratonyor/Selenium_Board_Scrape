from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date

class SimplyHired:
    def scrape(self, search_parameters, url):
        df_list = []
        for parameter in search_parameters:
            driver = webdriver.Chrome()
            driver.get(url.format(parameter))
            df_list.append(self.create_page_df(driver))
            # TODO Add next page functionality
        df = pd.concat(df_list, ignore_index=True).drop_duplicates(
            subset=["Job_Title", "Company", "Location"], keep="first"
        )
        return df

    def create_page_df(self, driver):
        title_elements = driver.find_elements(By.XPATH, "//h3[@class = 'jobposting-title']")
        company_elements = driver.find_elements(By.XPATH, "//span[@class = 'JobPosting-labelWithIcon jobposting-company']")
        location_elements = driver.find_elements(By.XPATH, "//span[@class = 'jobposting-location']")
        id_elements = driver.find_elements(By.XPATH, "//h3/a")
        urls = []
        titles = []
        companies = []
        locations = []
        for element in id_elements:
            urls.append(
                "https://www.simplyhired.ca/job/"
                + element.get_attribute("data-mdref")
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
