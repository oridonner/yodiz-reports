import yaml
import json
import uuid
import os
import sys
import datetime
import requests
from python.postgres_lib import postgres_connect as conn

def create_resource_url(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    basic_url = 'https://app.yodiz.com/api/rest/v1/projects/4/'
    resource_url = {}
    resource_url['headers']={}
    resource_url['headers']['api-key'] = api_key
    resource_url['headers']['api-token'] = api_token
    url = basic_url + resource
    if resource in ['releases' ,'sprints']:
        query = '?fields={0}'.format(fields)
    if resource in ['issues','userstories','users']:
        query = '?limit={0}&fields={1}&offset={2}'.format(limit,fields,offset)
    resource_url['url'] = url + query
    return resource_url
  
# get issues offset as input
def get_resource_list(resource,fields='all',limit=50,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    response = requests.get(url['url'],headers= url['headers'])  
    if resource in ['issues','userstories']:
        resource_list = response.json()[0]
    if resource in ['users','releases', 'sprints']:
        resource_list = response.json()
    return resource_list

def get_resource_count(resource,fields='all',limit=1,offset=0,api_key=None,api_token=None):
    url = create_resource_url(resource,fields,limit,offset,api_key,api_token)
    response = requests.get(url['url'],headers= url['headers']) 
    resource_dict = response.json()
    return resource_dict[1]['totalCount']

def load_resource(resource,fields='all',api_key=None,api_token=None,connection=None):
    start_time = datetime.datetime.now()
    guid = uuid.uuid4()
    if resource == 'userstories':
        resource_count = get_resource_count(resource=resource,api_key= api_key,api_token= api_token)
        iterations = divmod(resource_count,50)[0]
        if divmod(resource_count,50)[1]>0:
            iterations += 1
        i = 0
        while i < iterations:
            offset = i*50
            resource_list = get_resource_list(resource=resource,fields='all',limit=50,offset=offset,api_key=api_key,api_token=api_token)
            print 'iteration {0}: imported {1} - {2} from {3} {4}'.format(i,str(offset+1),str((i+1)*50),resource_count,resource)
            i +=1
            conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list)

    if resource == 'issues':
        # import issues
        resource_count = get_resource_count(resource=resource,api_key= api_key,api_token= api_token)
        iterations = divmod(resource_count,50)[0]
        if divmod(resource_count,50)[1]>0:
            iterations += 1
        i = 0
        while i < iterations:
            offset = i*50
            resource_list = get_resource_list(resource=resource,fields='all',limit=50,offset=offset,api_key=api_key,api_token=api_token)
            print 'iteration {0}: imported {1} - {2} from {3} {4}'.format(i,str(offset+1),str((i+1)*50),resource_count,resource)
            i +=1
            conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list) 
        
        #check for issues connected with userstory
        print 'checking for issues connected with userstory'
        basic_url = 'https://app.yodiz.com/api/rest/v1/userstories/'
        statement = 'select id from vw_userstories where isactive;'
        ust_list = conn.postgres_rows_select(connection = connection,statement=statement)
        for ust in ust_list:
            userstory=str(ust[0])
            url = basic_url + userstory + '/issues?fields=id'
            headers = {}
            headers['api-key'] = api_key
            headers['api-token'] = api_token
            try:
                response = requests.get(url,headers= headers)
                response.raise_for_status()
                resource_list = response.json()
                for item in resource_list:
                    conn.update_userstory_issue(connection=connection,issue_id=  item['id'],userstory_id=userstory )
                print 'update {0} issues of UserStory Id {1}'.format(str(len(resource_list)),userstory)
            except requests.exceptions.HTTPError as errh:
                pass
     

    if resource in ['users','releases','sprints']:
        resource_list = get_resource_list(resource=resource,api_key=api_key,api_token=api_token)
        conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list)

    if resource == 'tasks':
        basic_url = 'https://app.yodiz.com/api/rest/v1/userstories/'
        statement = 'select id from vw_userstories where isactive;'
        ust_list = conn.postgres_rows_select(connection = connection,statement=statement)
        for ust in ust_list:
            userstory=str(ust[0])
            url = basic_url + userstory + '/tasks?fields=all'
            headers = {}
            headers['api-key'] = api_key
            headers['api-token'] = api_token
            try:
                response = requests.get(url,headers= headers)
                response.raise_for_status()
                resource_list = response.json()
                for item in resource_list:
                    item['UserStoryId'] = ust[0]
                conn.postgres_block_insert(connection = connection,guid = guid, resource=resource,resource_list = resource_list)
                #conn.postgres_log_insert(connection=connection,guid=guid,iter=,resource,http_message)
                message = 'inserting {0} tasks from active UserStory Id {1}'.format(str(len(resource_list)),userstory)
            except requests.exceptions.HTTPError as errh:
                message = response.json()['message'] + ' id {0}'.format(userstory)
            print message
    
    statement = 'select count(*) from {0}'.format(resource)
    rows = conn.postgres_rows_select(connection = connection,statement=statement)
    end_time = datetime.datetime.now()
    load_time = end_time - start_time
    print "total {0} rows loaded to '{1}' table, duration: {2}".format(str(rows[0][0]),resource,load_time)
    print "load guid: {0}".format(guid)
    



