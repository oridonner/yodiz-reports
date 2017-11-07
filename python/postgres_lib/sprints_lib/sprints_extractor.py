from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn
import requests
import yaml
import os

def sprints_feedbak(connection):
    statement = 'select count(*) from sprints'
    result = conn.get_rows(connection,statement)
    return result[0]['count']
    

# get sprints list from yodiz api
def get_sprints_list(url_headers):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/sprints?fields=all'
    response = requests.get(url,headers=url_headers)
    sprints_list = response.json()
    return sprints_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_sprint_row(sprint_dict):
    sprint_row={}
    sprint_row['Id'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'id') else sprint_dict['id']
    sprint_row['Title'] = '' if not fnx.is_key_in_dictionary(sprint_dict,'title') else sprint_dict['title']
    sprint_row['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'owner','id') else sprint_dict['owner']['id']
    sprint_row['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'updatedOn') else  sprint_dict['updatedOn']
    sprint_row['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'createdOn') else sprint_dict['createdOn']
    sprint_row['Status'] = '' if not fnx.is_key_in_dictionary(sprint_dict,'status','narrative') else sprint_dict['status']['narrative']
    sprint_row['StartDate'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'startDate') else sprint_dict['startDate']
    sprint_row['EndDate'] = 'NULL' if not fnx.is_key_in_dictionary(sprint_dict,'endDate') else sprint_dict['endDate']
    return sprint_row

def insert_sprint_row(connection ,sprint_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into sprints(Id,Title,CreatedById,UpdatedOn,CreatedOn,Status,StartDate,EndDate) 
    values({0},'{1}',{2},'{3}','{4}','{5}','{6}','{7}');
    """
    insert_statement = insert_statement_template.format(
        sprint_row['Id'], #{0} int
        fnx.escape_postgres_string(sprint_row['Title']), #{1} text
        sprint_row['CreatedById'], #{2} int
        sprint_row['UpdatedOn'], #{3} timestamp without time zone
        sprint_row['CreatedOn'], #{4} timestamp without time zone
        sprint_row['Status'], #{5} text
        sprint_row['StartDate'], #{6} timestamp without time zone
        sprint_row['EndDate'] #{7} timestamp without time zone
        
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

def insert_sprints_table(connection,sprints_list):
    for sprint_dict in sprints_list:
        sprint_row = build_sprint_row(sprint_dict)
        insert_sprint_row(connection ,sprint_row)
    
def extract(connection,url_headers):
    sprints_list = get_sprints_list(url_headers)
    insert_sprints_table(connection,sprints_list)
    rows_extracted = sprints_feedbak(connection)
    print "{0} rows were inserted to 'sprints' table".format(rows_extracted)