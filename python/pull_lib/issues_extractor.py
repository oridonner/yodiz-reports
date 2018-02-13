import requests
import uuid
import sys
import os
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

# get num of rows inserted to issues table 
def issues_feedback(connection):
    statement = 'select count(*) from issues'
    result = conn.get_rows(connection,statement)
    return result[0]['count']

# get size of issues tabale from yodiz api
def get_issues_size(url_headers):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/issues?fields=all&limit=1&offset=0'
    lst = fnx.get_api_response(url_headers=url_headers,url=url)
    issues_size = lst[1]['totalCount']
    return issues_size

# get issues list from yodiz api, by offset
def get_issues_list_offset(config,url_headers,offset,transact_guid):
    url = 'https://app.yodiz.com/api/rest/v1/projects/4/issues?fields=all&limit=50&offset={0}'.format(offset)
    issues_list_partial = fnx.get_api_response(config,url_headers,url,transact_guid)[0]
    return issues_list_partial

# get full issues list from yodiz api
def get_issues_list(config,url_headers,transact_guid):
    issues_list = []
    issues_size = get_issues_size(url_headers)
    iterations = divmod(issues_size,50)[0]
    if divmod(issues_size,50)[1]>0:
        iterations += 1
    i = 0
    while i < iterations:
        offset = i*50
        issues_list_offset = get_issues_list_offset(config,url_headers,offset,transact_guid)
        issues_list += issues_list_offset
        print 'iteration {0}: imported issues {1} - {2} from {3} into dict.'.format(i,str(offset+1),str((i+1)*50),issues_size)
        i +=1
    return issues_list

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_issue_row(transact_guid,issue_dict):
    issue_row={}
    issue_row['Guid'] = transact_guid
    issue_row['Id'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'id') else issue_dict['id']
    issue_row['Title'] = '' if not fnx.is_key_in_dictionary(issue_dict,'title') else issue_dict['title']
    issue_row['UserStoryId'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'UserStoryId') else issue_dict['UserStoryId'] #inserted by code
    issue_row['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'createdBy','id') else issue_dict['createdBy']['id']
    issue_row['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'updatedOn') else  issue_dict['updatedOn']
    issue_row['UpdatedById'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'updatedBy','id') else  issue_dict['updatedBy']['id']
    issue_row['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'createdOn') else issue_dict['createdOn']
    issue_row['ResponsibleId'] =  'NULL' if not fnx.is_key_in_dictionary(issue_dict,'responsible','id') else issue_dict['responsible']['id']
    issue_row['Status'] = '' if not fnx.is_key_in_dictionary(issue_dict,'status','narrative') else issue_dict['status']['narrative']
    issue_row['Severity'] = '' if not fnx.is_key_in_dictionary(issue_dict,'severity','narrative') else issue_dict['severity']['narrative']
    issue_row['ReleaseId'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'release','id') else issue_dict['release']['id']
    issue_row['SprintId'] = 'NULL' if not fnx.is_key_in_dictionary(issue_dict,'sprint','id') else issue_dict['sprint']['id']
    issue_row['EffortEstimate'] = '' if not fnx.is_key_in_dictionary(issue_dict,'effortEstimate') else issue_dict['effortEstimate']
    issue_row['EffortRemaining'] = '' if not fnx.is_key_in_dictionary(issue_dict,'effortRemaining') else issue_dict['effortRemaining']
    issue_row['EffortLogged'] = '' if not fnx.is_key_in_dictionary(issue_dict,'effortLogged') else issue_dict['effortLogged']
    return issue_row

def insert_issue_row(connection ,issue_row):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Issues(Guid,Id,Title,UserStoryId,CreatedById,UpdatedOn,UpdatedById,CreatedOn,ResponsibleId,Status,Severity,ReleaseId,SprintId,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},'{2}',{3},{4},'{5}',{6},'{7}',{8},'{9}','{10}',{11},{12},{13},{14},{15});
    """
    insert_statement = insert_statement_template.format(
        issue_row['Guid'], #{0} text
        issue_row['Id'], #{1} int
        fnx.escape_postgres_string(issue_row['Title']), #{2} text
        issue_row['UserStoryId'], #{3} int        
        issue_row['CreatedById'], #{4} int
        issue_row['UpdatedOn'], #{5} timestamp without time zone
        issue_row['UpdatedById'], #{6} int
        issue_row['CreatedOn'], #{7} timestamp without time zone
        issue_row['ResponsibleId'], #{8} int
        issue_row['Status'], #{9} text
        issue_row['Severity'], #{10} text
        issue_row['ReleaseId'], #{11} int
        issue_row['SprintId'], #{12} int
        issue_row['EffortEstimate'], #{13} real
        issue_row['EffortRemaining'], #{14} real
        issue_row['EffortLogged'] #{15} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

# insert release rows to create full table
def insert_issues_table(connection,issues_list,transact_guid):   
    for issue_dict in issues_list:
        issue_row = build_issue_row(transact_guid,issue_dict)
        insert_issue_row(connection ,issue_row)

# this function is being called by yodiz.py
def extract(config,url_headers,transact_guid):
    issues_list = get_issues_list(config,url_headers,transact_guid)
    connection = conn.postgres_connect(config)
    insert_issues_table(connection,issues_list,transact_guid)
    rows_inserted = issues_feedback(connection)
    table_name = 'issues'
    action = 'insert'
    database = config['postgres']['dbname']
    conn.update_db_log(connection,transact_guid,table_name,action,rows_inserted)
    print "{0} rows were inserted to 'issues' table in {1} database".format(rows_inserted,database)