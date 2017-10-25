import yaml
import os

from python.general_lib import fnx


#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_row_dict(guid,resource_dict):
    row_dict={}
    row_dict['Guid'] = guid
    row_dict['Id'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'id') else resource_dict['id']
    row_dict['Title'] = '' if not fnx.is_key_in_dictionary(resource_dict,'title') else resource_dict['title']
    row_dict['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'createdBy','id') else resource_dict['createdBy']['id']
    row_dict['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'updatedOn') else  resource_dict['updatedOn']
    row_dict['UpdatedById'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'updatedBy','id') else  resource_dict['updatedBy']['id']
    row_dict['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'createdOn') else resource_dict['createdOn']
    row_dict['ResponsibleId'] =  'NULL' if not fnx.is_key_in_dictionary(resource_dict,'responsible','id') else resource_dict['responsible']['id']
    row_dict['Status'] = '' if not fnx.is_key_in_dictionary(resource_dict,'status','narrative') else resource_dict['status']['narrative']
    row_dict['Severity'] = '' if not fnx.is_key_in_dictionary(resource_dict,'severity','narrative') else resource_dict['severity']['narrative']
    row_dict['ReleaseId'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'release','id') else resource_dict['release']['id']
    row_dict['SprintId'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'sprint','id') else resource_dict['sprint']['id']
    row_dict['EffortEstimate'] = '' if not fnx.is_key_in_dictionary(resource_dict,'effortEstimate') else resource_dict['effortEstimate']
    row_dict['EffortRemaining'] = '' if not fnx.is_key_in_dictionary(resource_dict,'effortRemaining') else resource_dict['effortRemaining']
    row_dict['EffortLogged'] = '' if not fnx.is_key_in_dictionary(resource_dict,'effortLogged') else resource_dict['effortLogged']
    return row_dict

