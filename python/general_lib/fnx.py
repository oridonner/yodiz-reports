import email
import yaml
import smtplib
import requests
import os
from python.postgres_lib import postgres_connect as conn

def is_key_in_dictionary(d,n1,n2 = None,n3=None):
    if n1 not in d:
        return False
    if n2 is not None and n2 not in d[n1]:
        return False
    if n3 is not None and n3 not in d[n1][n2]:
        return False
    return True

def escape_postgres_string(string):
    return string.replace("'", "''")  

def get_full_path(file):
    name = os.path.basename(file)
    full_path = os.path.abspath(file)
    path = full_path.split(name,1)[0]
    return path

def import_config(file):
    file_path = get_full_path(file)
    file_name = file_path + '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_api_response(config,url_headers,url,transact_guid):
    db_conn = conn.postgres_connect(config)
    response = requests.get(url,headers=url_headers)
    lst = response.json()
    response_code = response.status_code
    if response_code == 200:
        response_text = 'Data pull succeeded'
    else:
        response_text = response.text
        # write to log
    conn.update_api_log(db_conn,transact_guid,url,response_code,response_text)
    return lst