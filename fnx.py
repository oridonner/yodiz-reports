#!/usr/bin/env python2.7
import os 
import sys
import json
import yaml
import datetime
import operator
from python.yodiz_lib import pull
from python.yodiz_lib import mail
from python.postgres_lib.releases_lib import releases_mapper
from python.postgres_lib.releases_lib import releases_loader
from python.postgres_lib import postgres_connect as conn
from python.yodiz_lib import arg_parser

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

    config = import_config()
    connection = conn.postgres_connect(dbname=config['postgres']['dbname'],user=config['postgres']['user'],password=config['postgres']['password'],host=config['postgres']['host'],port=config['postgres']['port'])
<<<<<<< HEAD
    fields_list = conn.get_table_culomns(connection,'vw_userstories_tot')
    #statement = 'select * from vw_userstories_tot'
    #row_list = conn.postgres_rows_select(connection, statement)
    mail.email_sprints(connection,fields_list)
=======
    statement = 'select * from vw_sprints_sub_tot'
    #print conn.get_rows(connection,statement)
    #print conn.get_table_culomns(connection,'vw_sprints_sub_tot')
    result = conn.get_rows(connection , 'select count(*) from sprints')
    print result[0]['count']
    #print conn.postgres_rows_select(connection,statement)
    #print params.issues
    #print args
    # if params.cmd_object == 'pull':
    #     if params.resource:
    #         print 'yes'
    # if params.cmd_object == 'mail':
    #     print params.mailinglist
    #statement = 'select * from vw_userstories_tot'
    #row_list = conn.postgres_rows_select(connection, statement)
    #mail.email_sprints(connection,fields_list)
>>>>>>> master
    #html = mail.sprints_to_html_table('test',fields_list,row_list)

    
if __name__ == "__main__":
    main()
