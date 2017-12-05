import email
import yaml
import smtplib
import requests
import os
from python.general_lib import postgres_connect as conn

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
    file_path = os.path.join(file_path,'.yodiz')
    file_path = os.path.join(file_path,'.config')
    with open(file_path,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_api_response(config=None,url_headers=None,url=None,transact_guid=None):
    response = requests.get(url,headers=url_headers)
    lst = response.json()
    response_code = response.status_code
    if response_code == 200:
        response_text = 'Data pull succeeded'
    else:
        response_text = response.text
        # write to log
    if config is not None:
        db_conn = conn.postgres_connect(config)
        conn.update_api_log(db_conn,transact_guid,url,response_code,response_text)
    return lst

# general send email function
def send_email(subject, html_table,to_list=None,cc_list=None):
    if to_list is None:
        to_list = ['orid@sqreamtech.com']
    if cc_list is None:
        cc_list = ['ori@sqreamtech.com']
    msg = email.mime.Multipart.MIMEMultipart()
    body = email.mime.Text.MIMEText(html_table ,'html')
    # append two lists into one before converting each list to string
    recips_list = cc_list + to_list
    to_str = ','.join(to_list)
    cc_str = ','.join(cc_list)
    msg.attach(body)
    msg['From']    = 'zbabira@sqreamtech.com'
    msg['To'] = to_str
    msg['Cc'] = cc_str
    
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('zbabira@gmail.com','sqreamzbabira')
    server.sendmail('no-reply@sqreamtech.com', recips_list, msg.as_string())
    server.quit()
    message = "email {0} successfully sent To: {1} Cc: {2}".format(subject,to_str,cc_str)
    print message
