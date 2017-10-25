import psycopg2
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


def postgres_connect(postgres_dbname,postgers_user,postgres_password,postgres_host,postgres_port):
    connection_string = "dbname={0} user={1} password={2} host={3} port={4}".format(postgres_dbname,postgers_user,postgres_password,postgres_host,postgres_port)
    connection = psycopg2.connect(connection_string)
    return connection

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
            userstories_loader.postgres_row_insert(connection ,row_dict)
        if resource == 'users':
            row_dict = users_mapper.build_row_dict(resource_dict = resource_dict)
            users_loader.postgres_row_insert(connection ,row_dict)
