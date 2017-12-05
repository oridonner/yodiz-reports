#!/usr/bin/env python2.7
import os 
import sys
import yaml
import uuid
import subprocess

from python.general_lib import postgres_connect as conn
from python.general_lib import arg_parser as argp
from python.mail_lib import sprints_mail
from python.mail_lib import capacity_mail
from python.mail_lib import inv_mail
from python.mail_lib import release_mail

from python.pull_lib import sprints_extractor
from python.pull_lib import releases_extractor
from python.pull_lib import users_extractor
from python.pull_lib import issues_extractor
from python.pull_lib import tasks_extractor
from python.pull_lib import userstories_extractor
from python.general_lib import fnx

def main():
    config = fnx.import_config(__file__)  
    dbname = config['postgres']['dbname']
    port = config['postgres']['port']
    host = config['postgres']['host']
    user = config['postgres']['user']
    project_path = config['project']['path']
    project_name = config['project']['name']
    project_full_path = os.path.join(project_path,project_name)
    html_lib = os.path.join(project_path,'.yodiz/debug/html/')
    
    python = config['prerequisites']['python']
    params = argp.params()
    connection = conn.postgres_connect(config)
    if params.cmd_object == 'build':
        if params.ddl:
            subprocess.Popen(".yodiz/build/database_build.sh")
        if params.database:
            subprocess.Popen(".yodiz/build/database_build.sh")
            subprocess.Popen("psql -h {0} -p {1} -U {2} -a -f .yodiz/build/database_build.sql".format(host,port,user))
        if params.views:
            subprocess.Popen(".yodiz/build/views_build.sh")
            print "creates and executes views_build.sql file"
            statement = "/usr/local/sqream-prerequisites/versions/3.04/bin/psql -h {0} -p {1} -U {2} -d {3} -a -f {4}.yodiz/build/views_build.sql".format(host,port,user,dbname,project_path)
            os.system(statement)
            
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
            sprints_mail.send(config,params.mailing_list,params.output_file)
        if params.capacity:
            capacity_mail.send(config,params.mailing_list,params.output_file)        
        if params.release:
            release_mail.send(config,params.mailing_list)
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
                #html_file = open("/home/orid/Documents/projects/Yodiz/.yodiz/debug/html/capacity.html","w")
