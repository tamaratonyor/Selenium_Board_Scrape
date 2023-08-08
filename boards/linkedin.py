import requests
from datetime import date
import pandas as pd
import json


class LinkedIn:
    def read_config(self, search_parameter):
        with open("./boards/headers/linkedin_header.json", "r") as f:
            header = json.load(f)
            header["path"] = header["path"].format(search_parameter)
        return header

    def create_page_df(self, titles, companies, locations, urls):
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

    def scrape(self, search_parameters, url):
        df_list = []
        for parameter in search_parameters:
            header = self.read_config(parameter)
            response = requests.get(url, headers=header)
            data = response.json()["included"]
            postings = []
            for job in data:
                if job.get("preDashNormalizedJobPostingUrn") is not None:
                    postings.append(job)
            titles = [posting["jobPostingTitle"] for posting in postings]
            companies = [posting["primaryDescription"]["text"] for posting in postings]
            locations = [
                posting["secondaryDescription"]["text"] for posting in postings
            ]
            urls = [
                "https://www.linkedin.com/jobs/view/"
                + posting["*jobPosting"].replace("urn:li:fsd_jobPosting:", "")
                for posting in postings
            ]
            df_list.append(self.create_page_df(titles, companies, locations, urls))
        df = pd.concat(df_list, ignore_index=True).drop_duplicates(
            subset=["Job_Title", "Company", "Location"], keep="first"
        )
        return df

'''if __name__ == "__main__":
    df = LinkedIn().scrape(["Remote%20Data%20Engineer","Remote%20AWS%20Engineer","Remote%20Big%20Data%20Engineer","Remote%20Hadoop%20Engineer","Remote%20Cloud%20Engineer", "Remote%20Azure%20Engineer", "Remote%20GCP%20Engineer", "Remote%20Pyspark%20Engineer"],
            "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-170&count=25&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_OTHER_ENTRY,keywords:{0},locationUnion:(geoId:101174742),spellCorrectionEnabled:true)&start=25"
    )
    print(df.shape[0])'''