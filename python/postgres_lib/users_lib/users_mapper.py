import yaml
import os

from python.general_lib import fnx


#inserts data from yodiz api to postgres dict, enters null if value doesn't exist 
def build_row_dict(resource_dict):
    row_dict={}
    row_dict['Id'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'id') else resource_dict['id']
    row_dict['FirstName'] = '' if not fnx.is_key_in_dictionary(resource_dict,'firstName') else resource_dict['firstName']
    row_dict['LastName'] = '' if not fnx.is_key_in_dictionary(resource_dict,'lastName') else resource_dict['lastName']
    row_dict['UpdatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'updatedOn') else  resource_dict['updatedOn']
    row_dict['CreatedOn'] = 'NULL' if not fnx.is_key_in_dictionary(resource_dict,'createdOn') else resource_dict['createdOn']
    return row_dict