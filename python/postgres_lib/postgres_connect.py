import psycopg2
import subprocess
import json
import os
from issues_lib import issues_mapper
from issues_lib import issues_loader
from userstories_lib import userstories_mapper
from userstories_lib import userstories_loader
from tasks_lib import tasks_mapper
from tasks_lib import tasks_loader
from users_lib import users_mapper
from users_lib import users_loader
from releases_lib import releases_mapper
from releases_lib import releases_loader
from sprints_lib import sprints_mapper
from sprints_lib import sprints_loader

def postgres_connect(dbname,user,password,host,port):
    connection_string = "dbname={0} user={1} password={2} host={3} port={4}".format(dbname,user,password,host,port)
    connection = psycopg2.connect(connection_string)
    return connection

# this function returns rows from postgres db 
def postgres_rows_select(connection , statement):
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    
    result = cur.fetchall()
    return result

def execute_statement(connection , statement):
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    

# this function truncates table in postgres
def truncate_table(connection, table_name):
    cur = connection.cursor()
    statement = 'truncate table {0}'.format(table_name)
    cur.execute(statement)
    print cur.query
    connection.commit()

def drop_table(connection, table_name):
    cur = connection.cursor()
    statement = 'drop table if exists {0} cascade'.format(table_name)
    cur.execute(statement)
    print cur.query
    connection.commit()

# this function truncates table inpostgres
def create_table(connection, table_name):
    cur = connection.cursor()
    file_name = 'tbl_{0}.sql'.format(table_name)
    file_path = os.path.join('postgres',table_name,file_name)
    print file_path
    cur.execute(open(file_path,'r').read())
    print cur.query
    connection.commit()

def postgres_block_insert(connection, guid ,resource,resource_list):
    for resource_dict in resource_list:
        if resource == 'issues':
            row_dict = issues_mapper.build_row_dict(guid = guid,resource_dict = resource_dict)
            issues_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'userstories':
            row_dict = userstories_mapper.build_row_dict(guid = guid,resource_dict = resource_dict)
            userstories_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'tasks':
            row_dict = tasks_mapper.build_row_dict(guid = guid,resource_dict = resource_dict)
            tasks_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'users':
            row_dict = users_mapper.build_row_dict(resource_dict = resource_dict)
            users_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'releases':
            row_dict = releases_mapper.build_row_dict(guid = guid,resource_dict = resource_dict)
            releases_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'sprints':
            row_dict = sprints_mapper.build_row_dict(guid = guid,resource_dict = resource_dict)
            sprints_loader.postgres_row_insert(connection ,row_dict)
def postgres_log_insert(connection,guid,iter,resource,http_message):
    
    pass    

def create_table_objects(connection,table_name):
    cur = connection.cursor()
    file_name = '{0}_builder.sql'.format(table_name)
    file_path = os.path.join('postgres/build',file_name)
    print file_path
    cur.execute(open(file_path,'r').read())
    print cur.query
    connection.commit()

def update_userstory_issue(connection,issue_id,userstory_id):
    cur = connection.cursor()
    statement = 'update issues set userstoryid = {0} where id = {1}'.format(userstory_id,issue_id)
    cur.execute(statement)
    connection.commit()