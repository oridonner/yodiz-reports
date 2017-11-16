import yaml
import os

from python.general_lib import fnx


#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_row_dict(guid,resource_dict):
    row_dict={}
    row_dict['Guid'] = guid
    row_dict['TaskId'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'id') else resource_dict['id']
    row_dict['UserStoryId'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'id') else resource_dict['UserStoryId'] # inserted from code
    row_dict['Title'] = '' if not fnx.is_key_in_dictionary(resource_dict,'title') else resource_dict['title']
    row_dict['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'createdBy','id') else resource_dict['createdBy']['id']
    row_dict['UpdatedOn'] = "2099-12-31T13:56:02-07:00" if not fnx.is_key_in_dictionary(resource_dict,'updatedOn') else  resource_dict['updatedOn']
    row_dict['UpdatedById'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'updatedBy','id') else  resource_dict['updatedBy']['id']
    row_dict['CreatedOn'] = "2099-12-31T13:56:02-07:00" if not fnx.is_key_in_dictionary(resource_dict,'createdOn') else resource_dict['createdOn']
    row_dict['Status'] = '' if not fnx.is_key_in_dictionary(resource_dict,'status','code') else resource_dict['status']['code']
    row_dict['EffortEstimate'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'effortEstimate') else resource_dict['effortEstimate']
    row_dict['EffortRemaining'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'effortRemaining') else resource_dict['effortRemaining']
    row_dict['EffortLogged'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'effortLogged') else resource_dict['effortLogged']
    return row_dict