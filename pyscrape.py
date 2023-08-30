import pandas as pd
import sqlalchemy
import json
from boards.indeed import Indeed
from boards.simplyhired import SimplyHired
from boards.linkedin import LinkedIn
import logging
from selenium import webdriver


def get_connection(
    database_user, database_password, database_port, database_name, database_ip
):
    database_connection = sqlalchemy.create_engine(
        "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            database_user, database_password, database_ip, database_port, database_name
        )
    )
    return database_connection


def read_table(database_connection):
    df = pd.read_sql_table("JobPostings_DataEngineer", database_connection)
    return df


def read_config():
    with open("./config/config.json", "r") as f:
        config = json.load(f)
    return config


def dedup(df_list):
    deduped_df = pd.concat(df_list, ignore_index=True).drop_duplicates(
        subset=["Job_Title", "Company"], keep="first"
    )
    return deduped_df


if __name__ == "__main__":
    config = read_config()
    connection = config["Connection"]
    search_parameters = config["SearchParameters"]
    web_urls = config["URLs"]
    database_connection = get_connection(
        connection["Username"],
        connection["Password"],
        connection["Port"],
        connection["DbName"],
        connection["IP"],
    )
    df_list = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    for url in web_urls:
        if "indeed" in url:
            df_list.append(
                Indeed().scrape(
                    driver=driver, search_parameters=search_parameters, url=url
                )
            )
        elif "simplyhired" in url:
            df_list.append(
                SimplyHired().scrape(
                    driver=driver, search_parameters=search_parameters, url=url
                )
            )
        elif "linkedin" in url:
            df_list.append(
                LinkedIn().scrape(
                    driver=driver, search_parameters=search_parameters, url=url
                )
            )
        else:
            logging.error(
                "Unsupported Job Board! Please edit the config json accordingly."
            )
    current_df = dedup(df_list)
    historical_df = read_table(database_connection)
    deduped_df = dedup([historical_df, current_df])
    deduped_df.to_sql(
        con=database_connection,
        name="JobPostings_DataEngineer",
        if_exists="replace",
        index=False,
    )
