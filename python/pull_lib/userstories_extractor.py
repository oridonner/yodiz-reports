import requests
import uuid
import os
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

# get num of rows inserted to userstories table 
def userstories_feedback(connection):
    statement = 'select count(*) from userstories'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get size of userstories tabale from yodiz api
def get_userstories_size(url_headers):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/userstories?fields=all&limit=1&offset=0'
    lst = fnx.get_api_response(url_headers=url_headers,url=url)
    userstories_size = lst[1]['totalCount']
    return userstories_size

# get userstories list from yodiz api, by offset
def get_userstories_list_offset(config,url_headers,offset,transact_guid):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/userstories?fields=all&limit=50&offset={0}'.format(offset)
    userstories_list_partial = fnx.get_api_response(config,url_headers,url,transact_guid)[0]
    return userstories_list_partial

# get full userstories list from yodiz api
def get_userstories_list(config,url_headers,transact_guid):
    userstories_list = []
    userstories_size = get_userstories_size(url_headers)
    iterations = divmod(userstories_size,50)[0]
    if divmod(userstories_size,50)[1]>0:
        iterations += 1
    i = 0
    while i < iterations:
        offset = i*50
        userstories_list_offset = get_userstories_list_offset(config,url_headers,offset,transact_guid)
        userstories_list += userstories_list_offset
        print 'iteration {0}: imported userstories {1} - {2} from {3}'.format(i,str(offset+1),str((i+1)*50),userstories_size)
        i +=1
    return userstories_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_userstory_row(transact_guid,userstory_dict):
    userstory_row={}
    userstory_row['Guid'] = transact_guid
    userstory_row['Id'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'id') else userstory_dict['id']
    userstory_row['Title'] = '' if not fnx.is_key_in_dictionary(userstory_dict,'title') else userstory_dict['title']
    userstory_row['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'createdBy','id') else userstory_dict['createdBy']['id']
    userstory_row['UpdatedOn'] = '' if not fnx.is_key_in_dictionary(userstory_dict,'updatedOn') else  userstory_dict['updatedOn']
    userstory_row['UpdatedById'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'updatedBy') else  userstory_dict['updatedBy']['id']
    userstory_row['CreatedOn'] = '' if not fnx.is_key_in_dictionary(userstory_dict,'createdOn') else userstory_dict['createdOn']
    userstory_row['ResponsibleId'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'owner','id') else userstory_dict['owner']['id']
    userstory_row['Status'] = '' if not fnx.is_key_in_dictionary(userstory_dict,'status','narrative') else userstory_dict['status']['narrative']
    userstory_row['ReleaseId'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'release','id') else userstory_dict['release']['id']
    userstory_row['SprintId'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'sprint','id') else userstory_dict['sprint']['id']
    userstory_row['EffortEstimate'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'effortEstimate') else userstory_dict['effortEstimate']
    userstory_row['EffortRemaining'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'effortRemaining') else userstory_dict['effortRemaining']
    userstory_row['EffortLogged'] = 'NULL' if not fnx.is_key_in_dictionary(userstory_dict,'effortLogged') else userstory_dict['effortLogged']
    return userstory_row

def insert_userstory_row(connection ,userstory_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into UserStories(Guid,Id,Title,CreatedById,UpdatedOn,UpdatedById,CreatedOn,ResponsibleId,Status,ReleaseId,SprintId,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},'{2}',{3},'{4}',{5},'{6}',{7},'{8}',{9},{10},{11},{12},{13});
    """
    insert_statement = insert_statement_template.format(
        userstory_row['Guid'], #{0} text
        userstory_row['Id'], #{1} int
        fnx.escape_postgres_string(userstory_row['Title']), #{2} text
        userstory_row['CreatedById'], #{3} int
        userstory_row['UpdatedOn'], #{4} timestamp without time zone
        userstory_row['UpdatedById'], #{5} int
        userstory_row['CreatedOn'], #{6} timestamp without time zone
        userstory_row['ResponsibleId'], #{7} int - owner in yodiz api 
        userstory_row['Status'], #{8} text
        userstory_row['ReleaseId'], #{9} int
        userstory_row['SprintId'], #{10} int
        userstory_row['EffortEstimate'], #{11} real
        userstory_row['EffortRemaining'], #{12} real
        userstory_row['EffortLogged'], #{13} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

# insert release rows to create full table
def insert_userstories_table(connection,userstories_list,transact_guid):
    for userstory_dict in userstories_list:
        userstory_row = build_userstory_row(transact_guid,userstory_dict)
        insert_userstory_row(connection ,userstory_row)

# this function is being called by yodiz.py
def extract(config,url_headers,transact_guid):
    connection = conn.postgres_connect(config)
    userstories_list = get_userstories_list(config,url_headers,transact_guid)
    insert_userstories_table(connection,userstories_list,transact_guid)
    table_name = 'userstories'
    action = 'insert'
    database = config['postgres']['dbname']
    rows_inserted = userstories_feedback(connection)
    conn.update_db_log(connection,transact_guid,table_name,action,rows_inserted)
    print "{0} rows were inserted to 'userstories' table in {1} database".format(rows_inserted,database)
