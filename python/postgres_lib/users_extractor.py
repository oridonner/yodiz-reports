import requests
import uuid
import yaml
import os
from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn

# get num of rows inserted to users table 
def users_feedback(connection):
    statement = 'select count(*) from users'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get sprints list from yodiz api
def get_users_list(url_headers):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/users'
    response = requests.get(url,headers=url_headers)
    users_list = response.json()
    return users_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_user_row(guid,users_dict):
    users_row={}
    users_row['Guid'] = guid
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
def insert_users_table(connection,users_list):
    guid = uuid.uuid4()
    for user_dict in users_list:
        user_row = build_user_row(guid,user_dict)
        insert_user_row(connection ,user_row)

# this function is being called by yodiz.py
def extract(connection,url_headers):
    users_list = get_users_list(url_headers)
    insert_users_table(connection,users_list)
    rows_extracted = users_feedback(connection)
    print "{0} rows were inserted to 'users' table".format(rows_extracted)



