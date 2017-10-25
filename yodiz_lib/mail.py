import sys
import email
import smtplib
from general_lib import fnx

# psql named views are located in spcripts folder
# {"resource": "query":"postgres named view"}
messages={}
messages['issues'] = {}
messages['issues']['severity'] = {}
messages['issues']['severity']['view'] = 'vw_open_issues_severity'
messages['issues']['severity']['subject'] = 'Bugs severity report'

messages['issues']['user'] = {}
messages['issues']['user']['view'] = 'vw_open_issues_per_user'
messages['issues']['user']['subject'] = 'Total bugs per user report'

messages['issues']['mtd'] = {}
messages['issues']['mtd']['view'] = 'vw_mtd_vs_pmtd_issues'
messages['issues']['mtd']['subject'] = 'Bugs closed vs. opened MTD report'

# general send email function
def email_result(subject, html_table):
    msg = email.mime.Multipart.MIMEMultipart()
    body = email.mime.Text.MIMEText(html_table , 'html')
    msg.attach(body)
    msg['From']    = 'zbabira@sqreamtech.com'
    msg['To'] = 'orid@sqreamtech.com'
    msg['Subject'] = subject
    recips = 'orid@sqreamtech.com'
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('zbabira@gmail.com','sqreamzbabira')
    server.sendmail('no-reply@sqreamtech.com', recips, msg.as_string())
    server.quit()

def build_html(html_tuple_list):
    html_list = [i[0] for i in html_tuple_list]
    html = ' '.join(html_list)
    return html

# get data fro postgres
def build_message(connection,statement):
    statement = "SELECT html_table('{0}')".format(statement)
    html_tuple_list = fnx.postgres_rows_select(connection,statement)
    html_table = build_html(html_tuple_list)
    return html_table

def send(resource,query,connection,messages=messages):
    statement = 'SELECT * FROM {0}'.format(messages[resource][query]['view'])
    html_table = build_message(connection,statement)
    email_result(messages[resource][query]['subject'],html_table)


