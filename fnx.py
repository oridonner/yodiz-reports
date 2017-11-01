#!/usr/bin/env python2.7
import os 
import sys
import json
import yaml
import datetime
from python.yodiz_lib import pull
from python.postgres_lib.releases_lib import releases_mapper
from python.postgres_lib.releases_lib import releases_loader
from python.postgres_lib import postgres_connect as conn

def import_config():
    file_name = '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def main():

    config = import_config()
    connection = conn.postgres_connect(dbname=config['postgres']['dbname'],user=config['postgres']['user'],password=config['postgres']['password'],host=config['postgres']['host'],port=config['postgres']['port'])
    #connection = conn.postgres_connect(postgres_dbname=postgres_dbname,postgers_user=postgers_user,postgres_password=postgres_password,postgres_host=postgres_host,postgres_port=postgres_port)
    releases_list =  pull.get_resource_list(resource= 'releases',api_key=config['yodiz']['api-key'],api_token=config['yodiz']['api-token'])
    for releases_dict in releases_list:
        release_row = releases_mapper.build_row_dict(guid='',resource_dict=releases_dict)
        releases_loader.postgres_row_insert(connection,release_row)
    #html_table = issues_query.get_total_open_issues(connection)
    #fnx.email_result(html_table)
    #print fnx.postgres_rows_select(connection,'SELECT open_bugs from total_open_bugs;')[0][0]
    main()