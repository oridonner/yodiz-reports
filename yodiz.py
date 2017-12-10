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
from python.general_lib import matplotlib_test as plot

def main():

    config = fnx.import_config(__file__)  
    connection = conn.postgres_connect(config)
    # statement = "select * from vw_sprints_headers"
    # sprint_chart_data = conn.postgres_rows_select(connection,statement)
    # for item in sprint_chart_data:
    #     print item
    #plot.build_sprint_chart(config,sprint_chart_data)
    #sys.exit(0)


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
    if params.cmd_object == 'build':
        db_object = ""
        if params.database:
            db_object= "database"
        if params.views:
            db_object= "views"
        if params.ddl:
            print "created {0} ddl file for database {1}".format(db_object,dbname)
            statement = "{0}.yodiz/build/{1}_build.sh".format(project_path,db_object)
            os.system(statement)
        if params.execute:
            print "executed {0} ddl file on database {1}".format(db_object,dbname)
            statement ="psql -h {0} -p {1} -d {2} -U {3} -a -f {4}.yodiz/build/{5}_build.sql".format(host,port,dbname,user,project_path,db_object)
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
