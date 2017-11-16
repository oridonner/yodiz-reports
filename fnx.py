#!/usr/bin/env python2.7
import os 
import sys
import json
import yaml
import uuid
import datetime
import operator
from python.postgres_lib import postgres_connect as conn
from python.yodiz_lib import arg_parser
from python.postgres_lib import issues_extractor as iss
def import_config():
    file_name = '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def set_status_color(status):
    return {
        'In Progress': "Yellow",
        'Done': "Green",
        'Blocked': "Red"
    }.get(status)

def main():
    transact_guid = uuid.uuid4()
    config = import_config()
    url_headers={}
    url_headers['api-key']= config['yodiz']['api-key']
    url_headers['api-token']= config['yodiz']['api-token']
    connection = conn.postgres_connect(dbname=config['postgres']['dbname'],user=config['postgres']['user'],password=config['postgres']['password'],host=config['postgres']['host'],port=config['postgres']['port'])
    iss.extract(connection,url_headers)
if __name__ == "__main__":
    main()
