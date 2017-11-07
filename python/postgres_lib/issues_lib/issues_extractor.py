from python.general_lib import fnx
import requests
import yaml
import os

#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_issue_row(guid,issue_dict):
    issue_row={}
    issue_row['Guid'] = guid
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
    return feedback_yodiz_issue_postgres()