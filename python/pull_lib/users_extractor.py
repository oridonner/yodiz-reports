import requests
import uuid
import yaml
import sys
import os
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

# get num of rows inserted to users table 
def users_feedback(connection):
    statement = 'select count(*) from users'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get sprints list from yodiz api
def get_users_list(config,url_headers,transact_guid):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/users'
    users_list = fnx.get_api_response(config,url_headers,url,transact_guid)
    return users_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_user_row(transact_guid,users_dict):
    users_row={}
    users_row['Guid'] = transact_guid
    users_row['Id'] = 'NULL' if not fnx.is_key_in_dictionary(users_dict,'id') else users_dict['id']
    users_row['FirstName'] = '' if not fnx.is_key_in_dictionary(users_dict,'firstName') else users_dict['firstName']
    users_row['LastName'] = '' if not fnx.is_key_in_dictionary(users_dict,'lastName') else users_dict['lastName']
    users_row['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(users_dict,'updatedOn') else  users_dict['updatedOn']
    users_row['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(users_dict,'createdOn') else users_dict['createdOn']
    return users_row

def insert_user_row(connection ,users_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Users(Guid,Id,FirstName,LastName,UpdatedOn,CreatedOn)
    values('{0}',{1},'{2}','{3}','{4}','{5}');
    """
    insert_statement = insert_statement_template.format(
        users_row['Guid'], #{0} text
        users_row['Id'], #{1} int
        users_row['FirstName'], #{2} text
        users_row['LastName'], #{3} text
        users_row['UpdatedOn'], #{4} timestamp without time zone
        users_row['CreatedOn'] #{5} timestamp without time zone
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()


# insert user rows to create full table
def insert_users_table(connection,users_list,transact_guid):
    for user_dict in users_list:
        user_row = build_user_row(transact_guid,user_dict)
        insert_user_row(connection,user_row)
    #set focusfactor
    statement = "update users set focusfactor = 0.5 where firstname in ('Ben','Ofer','Gil','Yuval')"
    conn.execute_statement(connection , statement)
    statement = "update users set focusfactor = 0.75 where firstname not in ('Ben','Ofer','Gil','Yuval')"
    conn.execute_statement(connection , statement)

# this function is being called by yodiz.py
def extract(config,url_headers,transact_guid):
    connection = conn.postgres_connect(config)
    users_list = get_users_list(config,url_headers,transact_guid)
    insert_users_table(connection,users_list,transact_guid)
    rows_inserted = users_feedback(connection)
    table_name = 'users'
    action = 'insert'
    database = config['postgres']['dbname']
    conn.update_db_log(connection,transact_guid,table_name,action,rows_inserted)
    print "{0} rows were inserted to 'users' table in {1} database".format(rows_inserted,database)
