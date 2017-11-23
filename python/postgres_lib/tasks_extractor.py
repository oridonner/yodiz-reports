import requests
import uuid
import time
import os
from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn

# get num of rows inserted to tasks table 
def tasks_feedback(connection):
    statement = 'select count(*) from tasks'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get userstory tasks list from yodiz api
def get_userstory_tasks_list(url_headers,userstory_id,connection,transact_guid):
    userstory_tasks_list = {}
    url = 'https://app.yodiz.com/api/rest/v1/userstories/' + str(userstory_id) + '/tasks?fields=all'
    response = requests.get(url,headers=url_headers)
    try:
        response = requests.get(url,headers= url_headers)
        response.raise_for_status()
        userstory_tasks_list = response.json()
        for item in userstory_tasks_list:
            item['UserStoryId'] = userstory_id
        #conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,userstory_tasks_list = userstory_tasks_list)
        #conn.postgres_log_insert(connection=connection,guid=guid,iter=,resource,http_message)
        message = 'inserting {0} tasks from active UserStory Id {1} into dict'.format(str(len(userstory_tasks_list)),userstory_id)
    except requests.exceptions.HTTPError as errh:
        print errh
        message = response.json()['message'] + ' id {0}'.format(userstory_id)
    print message
    response_code = response.status_code
    conn.update_api_log(connection,transact_guid,url,response_code,message)
    return userstory_tasks_list

#get active userstories id's from postgres
def get_userstories_ids(connection):
    statement = 'select userstory_id from vw_userstories where is_active'
    userstories_ids = conn.get_rows(connection,statement)
    return userstories_ids

# gather all tasks to one list
def get_tasks_list(url_headers,connection,transact_guid):
    tasks_list = []
    userstories_ids = get_userstories_ids(connection)
    for userstory_id in userstories_ids:
        userstory_tasks_list = get_userstory_tasks_list(url_headers,userstory_id['userstory_id'],connection,transact_guid)
        tasks_list += userstory_tasks_list
        time.sleep(60)
    return tasks_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_task_row(transact_guid,task_dict):
    task_row={}
    task_row['Guid'] = transact_guid
    task_row['TaskId'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'id') else task_dict['id']
    task_row['TaskOwnerId'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'owner','id') else task_dict['owner']['id']
    task_row['UserStoryId'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'id') else task_dict['UserStoryId'] # inserted from code
    task_row['Title'] = '' if not fnx.is_key_in_dictionary(task_dict,'title') else task_dict['title']
    task_row['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'createdBy','id') else task_dict['createdBy']['id']
    task_row['UpdatedOn'] = "2099-12-31T13:56:02-07:00" if not fnx.is_key_in_dictionary(task_dict,'updatedOn') else  task_dict['updatedOn']
    task_row['UpdatedById'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'updatedBy','id') else  task_dict['updatedBy']['id']
    task_row['CreatedOn'] = "2099-12-31T13:56:02-07:00" if not fnx.is_key_in_dictionary(task_dict,'createdOn') else task_dict['createdOn']
    task_row['Status'] = '' if not fnx.is_key_in_dictionary(task_dict,'status','code') else task_dict['status']['code']
    task_row['EffortEstimate'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'effortEstimate') else task_dict['effortEstimate']
    task_row['EffortRemaining'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'effortRemaining') else task_dict['effortRemaining']
    task_row['EffortLogged'] = 'NULL' if not fnx.is_key_in_dictionary(task_dict,'effortLogged') else task_dict['effortLogged']
    return task_row

def insert_task_row(connection ,task_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Tasks(Guid,TaskId,TaskOwnerId,UserStoryId,Title,CreatedById,UpdatedOn,UpdatedById,CreatedOn,Status,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},{2},{3},'{4}',{5},'{6}',{7},'{8}','{9}',{10},{11},{12});
    """
    insert_statement = insert_statement_template.format(
        task_row['Guid'], #{0} text
        task_row['TaskId'], #{1} int
        task_row['TaskOwnerId'], #{2} int
        task_row['UserStoryId'], #{3} int
        fnx.escape_postgres_string(task_row['Title']), #{4} text
        task_row['CreatedById'], #{5} int
        task_row['UpdatedOn'], #{6} timestamp without time zone
        task_row['UpdatedById'], #{7} int
        task_row['CreatedOn'], #{8} timestamp without time zone
        task_row['Status'], #{9} text
        task_row['EffortEstimate'], #{10} real
        task_row['EffortRemaining'], #{11} real
        task_row['EffortLogged'], #{12} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

# insert release rows to create full table
def insert_tasks_table(connection,tasks_list,transact_guid):
    for task_dict in tasks_list:
        task_row = build_task_row(transact_guid,task_dict)
        insert_task_row(connection ,task_row)

# this function is being called by yodiz.py
def extract(connection,url_headers,transact_guid):
    tasks_list = get_tasks_list(url_headers,connection,transact_guid)
    insert_tasks_table(connection,tasks_list,transact_guid)
    rows_inserted = tasks_feedback(connection)
    table_name = 'tasks'
    action = 'insert'
    conn.update_db_log(connection,transact_guid,table_name,action,rows_inserted)
    print "{0} rows were inserted to 'tasks' table".format(rows_inserted)
