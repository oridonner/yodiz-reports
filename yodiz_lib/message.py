import email
import smtplib
from general_lib import fnx


messages={}
messages['issues'] = {'open':'SELECT open_bugs from total_open_bugs'} 
messages['issues'] = {'severity':'SELECT open_bugs from total_open_bugs'} 


# general send email function
def email_result(html_table):
    msg = email.mime.Multipart.MIMEMultipart()
    body = email.mime.Text.MIMEText(html_table , 'html')
    msg.attach(body)
    msg['From']    = 'zbabira@sqreamtech.com'
    msg['To'] = 'orid@sqreamtech.com'
    msg['Subject'] = 'total open issues alert'
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

def send(message_name,connection):
    if message_name == 'total_issues':
        statement = 'SELECT open_bugs from total_open_bugs'
        html_table = build_message(connection,statement)
        email_result(html_table)
