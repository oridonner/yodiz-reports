import yaml
import json
import uuid
import os
import sys
import datetime
import requests
from python.postgres_lib import postgres_connect as conn

def create_resource_url(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    resource_url = {}
    resource_url['headers']={}
    resource_url['headers']['api-key'] = api_key
    resource_url['headers']['api-token'] = api_token
    if resource == 'releases':
        url = 'https://app.yodiz.com/api/rest/v1/projects/4/releases'
        query = '?limit={0}&fields={1}&offset={2}'.format(limit,fields,offset)
        resource_url['url'] = url + query
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
    if resource == 'users':
        resource_url['url'] = 'https://app.yodiz.com/api/rest/v1/projects/4/users'
    return resource_url
  
# get issues offset as input
def get_resource_list(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    response = requests.get(url['url'],headers= url['headers'])  
    if resource == 'issues':
        resource_list = response.json()[0]
    if resource == 'users':
        resource_list = response.json()
    if resource == 'releases':
        resource_list = response.json()
    return resource_list
 
def get_resource_count(resource,fields='all',limit=1,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    #print url
    response = requests.get(url['url'],headers= url['headers']) 
    #print response.json()
    resource_dict = response.json()
    
    return resource_dict[1]['totalCount']

def load_resource(resource,fields='all',api_key=None,api_token=None,connection=None):
    start_time = datetime.datetime.now()
    if resource == 'issues':
        resource_count = get_resource_count(resource=resource,api_key= api_key,api_token= api_token)
        iterations = divmod(resource_count,50)[0]
        if divmod(resource_count,50)[1]>0:
            iterations += 1
        i = 0
        while i < iterations:
            guid = uuid.uuid4()
            offset = i*50
            resource_list = get_resource_list(resource=resource,fields='all',limit=50,offset=offset,api_key=api_key,api_token=api_token)
            print 'iteration {0}: imported {1} - {2} from {3} {4}'.format(i,str(offset+1),str((i+1)*50),resource_count,resource)
            i +=1
            conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list)
    if resource == 'users':
        resource_list = get_resource_list(resource=resource,api_key=api_key,api_token=api_token)
        conn.postgres_block_insert(connection = connection,guid = None, resource=resource,resource_list = resource_list)
    if resource == 'releases':
        resource_list = get_resource_list(resource=resource,api_key=api_key,api_token=api_token)
        conn.postgres_block_insert(connection = connection,guid = None, resource=resource,resource_list = resource_list)
    end_time = datetime.datetime.now()
    load_time = end_time - start_time
    print 'load duration: {0}'.format(load_time)
    



