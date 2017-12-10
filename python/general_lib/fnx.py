import email
import yaml
import uuid
import smtplib
import requests
import cgi
import sys
import os
from python.general_lib import postgres_connect as conn
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header 

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
        cc_list = ['yuval@sqreamtech.com']
    msg = MIMEMultipart()
    body = MIMEText(html_table ,'html')
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

def send_email_image():
    msg = MIMEMultipart('related')
    img = dict(title="Picture report", path="/home/orid/Documents/projects/Yodiz/temp/un.png", cid=str(uuid.uuid4()))
    msg['From'] = 'zbabira@sqreamtech.com'
    msg['To'] = 'orid@sqreamtech.com'
    msg['Subject'] = 'image test'

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_text = MIMEText('[image: {title}]'.format(**img), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)
    msg_html_text = """
                        <html>
                        <head>
                            <style>h1 {{color: black; font-weight:bold; text-align: center;}}label {{color: darkgreen;}}table {{border-collapse: collapse;width: 100%;}}th {{text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}}</style>
                        </head>
                            <body>
                                <h1>Daily Sprint Report</h1>
                                    <div dir="ltr">
                                        <img src="cid:"{cid} alt="{title}"></img>
                                        <br>
                                    </div>
                                    <div style="display: inline-block">
                                        <div style="float: left;">
                                            <table style="width: 30%">
                                                <tr>
                                                        <th style='text-align: left;padding: 8px;background-color:black;color:white;'>Category</th>
                                                        <th style='text-align: left;padding: 8px;background-color:black;color:white;'>Total</th>
                                                        <th style='text-align: left;padding: 8px;background-color:black;color:white;'>#Completed</th>
                                                        <th style='text-align: left;padding: 8px;background-color:black;color:white;'>%Completed</th>
                                                </tr>
                                                <tr style="border-style:solid">
                                                    <td  style='padding:5px'>Sprint Days</td>
                                                    <td  style='padding:5px'>12</td>
                                                    <td  style='padding:5px'>3</td>
                                                    <td  style='padding:5px'>25%</td>
                                                </tr>
                                                <tr style="border-style:solid">                                    
                                                    <td  style='padding:5px'>Sprint Effort</td>                                       
                                                    <td  style='padding:5px'>33.5</td>                                        
                                                    <td  style='padding:5px'>3.0</td>                                       
                                                    <td  style='padding:5px'>9%</td>                                        
                                                </tr>
                                                <tr style="border-style:solid">
                                                    <td  style='padding:5px'>Userstories</td>
                                                    <td  style='padding:5px'>7</td>
                                                    <td  style='padding:5px'>0</td>
                                                    <td  style='padding:5px'>0%</td>
                                                </tr>
                                            </table>
                                        </div>
                                    </div>
                                    <br/>
                                    <br/>
            
                        <table>
                            <tr>
                        <th>id</th>
                             <th>Userstory Title</th>
                             <th>Status</th>
                             <th>Tasks Total</th>
                             <th>Tasks Unplanned</th>
                             <th>Tasks In Progress</th>
                             <th>Tasks Completed</th>
                             <th>Tasks Completion Ratio</th>
                             <th>Effort Estimate</th>
                             <th>Effort Spent</th>
                             <th>Effort Remaining</th>
                         
                            </tr>
                      
                            <tr bgcolor="Yellow" style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1548' target='_blank'>1548</a></td>
                         
                                <td  style='padding:5px'>[Duplicate of US-1530] Rewrite &quot;insert into&quot; to execute only with chunk producers</td>
                             
                                <td  style='padding:5px'>In Progress</td>
                             
                                <td  style='padding:5px'>2</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>1</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>9.0</td>
                             
                                <td  style='padding:5px'>3.0</td>
                             
                                <td  style='padding:5px'>6.0</td>
                             
                            </tr>
                         
                            <tr bgcolor="Yellow" style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1549' target='_blank'>1549</a></td>
                         
                                <td  style='padding:5px'>[Duplicate of US-1529] Reduce memory usage for insert parsers</td>
                             
                                <td  style='padding:5px'>In Progress</td>
                             
                                <td  style='padding:5px'>2</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>1</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>0.5</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.5</td>
                             
                            </tr>
                         
                            <tr style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1540' target='_blank'>1540</a></td>
                         
                                <td  style='padding:5px'>Support non-printable delimiters (e.g. ASCII 1) in insert from CSV</td>
                             
                                <td  style='padding:5px'>Not Started</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                            </tr>
                         
                            <tr style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1526' target='_blank'>1526</a></td>
                         
                                <td  style='padding:5px'>Bug of ODBC padding '_' was found during SA POCs. Define the problem, design a solution that will pass ben's initial review, implement it and test it.</td>
                             
                                <td  style='padding:5px'>Not Started</td>
                             
                                <td  style='padding:5px'>2</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                            </tr>
                         
                            <tr style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1551' target='_blank'>1551</a></td>
                         
                                <td  style='padding:5px'>[Duplicate of US-1531] Insert Rechunker POC</td>
                             
                                <td  style='padding:5px'>Not Started</td>
                             
                                <td  style='padding:5px'>3</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>24.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>24.5</td>
                             
                            </tr>
                         
                            <tr style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1550' target='_blank'>1550</a></td>
                         
                                <td  style='padding:5px'>[Duplicate of US-1532] Reduce memory usage for insert compressors</td>
                             
                                <td  style='padding:5px'>Not Started</td>
                             
                                <td  style='padding:5px'>2</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.5</td>
                             
                            </tr>
                         
                            <tr style="border-style:solid">
                        
                                <td style='padding:5px'><a href='https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-1536' target='_blank'>1536</a></td>
                         
                                <td  style='padding:5px'>Rewrite &quot;network insert&quot; to execute only with chunk producers</td>
                             
                                <td  style='padding:5px'>Not Started</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0</td>
                             
                                <td  style='padding:5px'>0%</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                                <td  style='padding:5px'>0.0</td>
                             
                            </tr>
                         
                        </table>
                      
                            </body>
                    </html>
                    """.format(**img)

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_text = MIMEText('[image: {title}]'.format(**img), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)

    msg_html = MIMEText(msg_html_text,'html', 'utf-8')
    msg_alternative.attach(msg_html)

    with open(img['path'], 'rb') as file:
        msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
        msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))
        msg.attach(msg_image)


    recips = "orid@sqreamtech.com"
    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login('zbabira@gmail.com','sqreamzbabira')
    s.sendmail('no-reply@sqreamtech.com', recips, msg.as_string())
    s.quit()
