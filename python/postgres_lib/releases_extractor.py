import requests
import uuid
import yaml
import os
from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn

# get num of rows inserted to releases table 
def releases_feedback(connection):
    statement = 'select count(*) from releases'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get sprints list from yodiz api
def get_releases_list(url_headers,connection,transact_guid):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/releases?fields=all'
    response = requests.get(url,headers=url_headers)
    response_code = response.status_code
    releases_list = response.json()
    conn.update_api_log(connection,transact_guid,url,response_code)
    return releases_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_release_row(transact_guid,release_dict):
    release_row={}
    release_row['Guid'] = transact_guid
    release_row['Id'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'id') else release_dict['id']
    release_row['Title'] = '' if not fnx.is_key_in_dictionary(release_dict,'title') else release_dict['title']
    release_row['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'owner','id') else release_dict['owner']['id']
    release_row['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'updatedOn') else  release_dict['updatedOn']
    release_row['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'createdOn') else release_dict['createdOn']
    release_row['Status'] = '' if not fnx.is_key_in_dictionary(release_dict,'status','narrative') else release_dict['status']['narrative']
    release_row['StartDate'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'startDate') else release_dict['startDate']
    release_row['EndDate'] = 'NULL' if not fnx.is_key_in_dictionary(release_dict,'endDate') else release_dict['endDate']
    return release_row

# insert release row to yodizdb
def insert_release_row(connection ,release_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Releases(Guid,Id,Title,CreatedById,UpdatedOn,CreatedOn,Status,StartDate,EndDate) 
    values('{0}',{1},'{2}',{3},'{4}','{5}','{6}','{7}','{8}');
    """
    insert_statement = insert_statement_template.format(
        release_row['Guid'], #{0} text
        release_row['Id'], #{1} int
        fnx.escape_postgres_string(release_row['Title']), #{2} text
        release_row['CreatedById'], #{3} int
        release_row['UpdatedOn'], #{4} timestamp without time zone
        release_row['CreatedOn'], #{5} timestamp without time zone
        release_row['Status'], #{6} text
        release_row['StartDate'], #{7} timestamp without time zone
        release_row['EndDate'] #{8} timestamp without time zone
        
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

# insert release rows to create full table
def insert_releases_table(connection,releases_list,transact_guid):
    for release_dict in releases_list:
        release_row = build_release_row(transact_guid,release_dict)
        insert_release_row(connection ,release_row)

# this function is being called by yodiz.py
def extract(connection,url_headers,transact_guid):
    releases_list = get_releases_list(url_headers,connection,transact_guid)
    insert_releases_table(connection,releases_list,transact_guid)
    rows_inserted = releases_feedback(connection)
    table_name = 'releases'
    action = 'insert'
    conn.update_db_log(connection,transact_guid,table_name,action,rows_inserted)
    print "{0} rows were inserted to 'releases' table".format(rows_inserted)
