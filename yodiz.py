#!/usr/bin/env python2.7
import os 
import sys
import yaml
import uuid
from python.general_lib import postgres_connect as conn
from python.general_lib import arg_parser as argp
from python.mail_lib import sprints_mail
from python.mail_lib import tasks_mail
from python.mail_lib import inv_mail

from python.pull_lib import sprints_extractor
from python.pull_lib import releases_extractor
from python.pull_lib import users_extractor
from python.pull_lib import issues_extractor
from python.pull_lib import tasks_extractor
from python.pull_lib import userstories_extractor
from python.general_lib import fnx

def main():
    params = argp.params()
    config = fnx.import_config(__file__)  
    connection = conn.postgres_connect(config)

    if params.cmd_object == 'build':
        if params.table:
            conn.create_table_objects(connection,params.table)
        if params.show:
            conn.create_all_objects(connection,params.show)
    
    if params.cmd_object == 'pull':
        transact_guid = uuid.uuid4()
        url_headers={}
        url_headers['api-key']= params.key
        url_headers['api-token']= params.token
        table_name = params.resource
        if params.truncate:
            conn.truncate_table(config,table_name,transact_guid)
        if params.resource == 'sprints':
            sprints_extractor.extract(config,url_headers,transact_guid)
        if params.resource == 'releases':
            releases_extractor.extract(config,url_headers,transact_guid)
        if params.resource == 'users':
            users_extractor.extract(config,url_headers,transact_guid)
        if params.resource == 'issues':
            issues_extractor.extract(config,url_headers,transact_guid)
        if params.resource == 'userstories':
            userstories_extractor.extract(config,url_headers,transact_guid)
        if params.resource == 'tasks':
            tasks_extractor.extract(config,url_headers,transact_guid)
    
    if params.cmd_object == 'mail':
        if params.sprints:
            sprints_mail.send(config,params.mailing_list)
        if params.tasks:
            tasks_mail.send(config,params.mailing_list)
        if params.inv:
            inv_mail.send(config)

    if params.cmd_object == 'query':
        if params.sprints:
            statement = 'select * from {0}'.format(params.sprints) 
            rows = conn.get_rows(connection,statement)
            for row in rows:
                print 'sprint title: {0} , sprint id:{1}'.format(row['sprint_title'],row['sprint_id']) 

if __name__ == "__main__":
    main()
