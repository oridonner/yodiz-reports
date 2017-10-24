import yaml
import json
import uuid
import os
import sys
import requests
from postgres_lib import postgres_connect as conn
#from postgres_lib import issues_fields_mapper as mapper
#import yodiz_api_variables
#from postgres_lib import postgres_connection_handler as conn
#from postgres_lib import postgres_mapper as mapper
#from authentication_lib import yodiz_authentication as auth

#yodiz_api_vars = yodiz_api_variables. get_yodiz_api_variables()
yodiz_api_issues_request={}
yodiz_api_issues_request['headers']={"api-key": "083c5c49-c1cc-490b-bffa-58b6d457ab57", "api-token": "v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4"}
yodiz_api_issues_request['url'] = 'https://app.yodiz.com/api/rest/v1/projects/4/issues'

# def create_yodiz_api_token():
#     auth.create_yodiz_api_token()
# # yodiz_api_fields = create_yodiz_api_fields_query()


# def create_yodiz_api_query(fields=all,limit=50,offset=0):
#     http_query = '?limit={ }&fields={1}&offset={2}'.format(limit,fields,offset)
#     return http_query


def create_resource_url(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    resource_url = {}
    resource_url['headers']={}
    resource_url['headers']['api-key'] = api_key
    resource_url['headers']['api-token'] = api_token
    if resource == 'issues':
        url = 'https://app.yodiz.com/api/rest/v1/projects/4/issues'
        query = '?limit={0}&fields={1}&offset={2}'.format(limit,fields,offset)
        resource_url['url'] = url + query
    if resource == 'userstories':
        url = 'https://app.yodiz.com/api/rest/v1/projects/4/userstories'
        query = '?limit={0}&fields={1}&offset={2}'.format(limit,fields,offset)
        resource_url['url'] = url + query
    if resource == 'tasks':
        url = 'https://app.yodiz.com/api/rest/v1/userstories/1/tasks'
        query = '?limit={0}&fields={1}&offset={2}'.format(limit,fields,offset)
        resource_url['url'] = url + query    
    #print resource_url
    return resource_url
  
# get issues offset as input
def get_resource_list(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    response = requests.get(url['url'],headers= url['headers'])  
    resource_list = response.json()[0]
    return resource_list
 
def get_resource_count(resource,fields='all',limit=1,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    response = requests.get(url['url'],headers= url['headers']) 
    resource_dict = response.json()
    return resource_dict[1]['totalCount']

def load_resource(resource,fields='all',api_key=None,api_token=None,connection=None):
    resource_count = get_resource_count(resource=resource,api_key= api_key,api_token= api_token)
    iterations = divmod(resource_count,50)[0]
    if divmod(resource_count,50)[1]>0:
        iterations += 1
    i = 0
    while i < iterations:
        guid = uuid.uuid4()
        offset = (i+1)*50
        resource_list = get_resource_list(resource=resource,fields='all',limit=50,offset=offset,api_key=api_key,api_token=api_token)
        print 'imported {0} from {1} {2}'.format(str(offset),resource_count,resource)
        conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list)
        #mapper.build_row_dict(guid, resource_list = resource_list)
        i +=1




