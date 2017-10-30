import yaml
import os

from python.general_lib import fnx


#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_row_dict(guid,resource_dict):
    row_dict={}
    row_dict['Guid'] = guid
    row_dict['Id'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'id') else resource_dict['id']
    row_dict['Title'] = '' if not fnx.is_key_in_dictionary(resource_dict,'title') else resource_dict['title']
    row_dict['CreatedById'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'owner','id') else resource_dict['owner']['id']
    row_dict['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'updatedOn') else  resource_dict['updatedOn']
    row_dict['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'createdOn') else resource_dict['createdOn']
    row_dict['Status'] = '' if not fnx.is_key_in_dictionary(resource_dict,'status','narrative') else resource_dict['status']['narrative']
    row_dict['StartDate'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'startDate') else resource_dict['startDate']
    row_dict['EndDate'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'endDate') else resource_dict['endDate']
    return row_dict
