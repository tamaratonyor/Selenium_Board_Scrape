import pandas as pd
import sqlalchemy
import re
from datetime import datetime, timedelta
import json
from boards.indeed import Indeed
from boards.linkedin import LinkedIn
from boards.monster import Monster
from boards.simplyhired import SimplyHired
import logging

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

def scrape(search_parameters):
    #TODO Use selenium to scrape and change pages. And remove unneccessary libraries. Add a dedup strategy. Then replace the git repo with this more robust version
    for parameter in search_parameters:
        ...

def dedup(current):
    historical = read_table(db_connection)


if __name__ == '__main__':
    config = read_config()
    db_connection = config['Connection']
    search_parameters = config['SearchParameters']
    web_urls = config['URLs']
    db_connection = get_connection()
    for url in web_urls:
        if url.contains('monster'):
            Monster.scrape(search_parameters=search_parameters)
        elif url.contains('simplyhired'):
            SimplyHired.scrape(search_parameters=search_parameters)
        elif url.contains('linkedin'):
            LinkedIn.scrape(search_parameters=search_parameters)
        elif url.contains('indeed'):
            Indeed.scrape(search_parameters=search_parameters)
        else:
            logging.error("Unsupported Job Board! Please edit the config json accordingly.")
    
    
