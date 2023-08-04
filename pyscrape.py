from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
import re
from datetime import datetime, timedelta
import json


def get_connection(database_user, database_password, database_port, database_name, database_ip):
    database_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.
                                               format(database_user,database_password, database_ip, database_port, database_name))
    return database_connection

def read_table(database_connection):
    df = pd.read_sql_table('JobPostings_DataEngineer', database_connection)
    return df

def read_config():
    with open('./config/config.json', 'r') as f:
        config = json.load(f)
    return config

def scrape(search_parameters, df):
    #TODO Use selenium to scrape and change pages. And remove unneccessary libraries. Add a dedup strategy. Then replace the git repo with this more robust version
    for parameter in search_parameters:
        ...

if __name__ == '__main__':
    config = read_config()
    db_connection = config['Connection']
    search_parameters = config['SearchParameters']
    web_urls = config['URLs']
    db_connection = get_connection()
    df = read_table(db_connection)
    for url in web_urls:
        scrape(search_parameters=search_parameters, df=df)
    