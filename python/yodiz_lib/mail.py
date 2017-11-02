import sys
import email
import smtplib
#from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn
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

messages['userstories'] = {}
messages['userstories']['total'] = {}
messages['userstories']['total']['view'] = 'vw_userstories_tot'
messages['userstories']['total']['subject'] = 'Userstories total report'

# general send email function
def email_result(subject, html_table):
    msg = email.mime.Multipart.MIMEMultipart()
    body = email.mime.Text.MIMEText(html_table , 'html')
    msg.attach(body)
    msg['From']    = 'zbabira@sqreamtech.com'
    msg['To'] = 'yuval@sqreamtech.com'
    msg['Subject'] = subject
    recips = 'yuval@sqreamtech.com'
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('zbabira@gmail.com','sqreamzbabira')
    server.sendmail('no-reply@sqreamtech.com', recips, msg.as_string())
    server.quit()

def build_html(html_tuple_list):
    html_list = [i[0] for i in html_tuple_list]
    html = ' '.join(html_list)
    return html

# get data from postgres
def build_message(connection,statement):
    statement = "SELECT html_table('{0}')".format(statement)
    html_tuple_list = conn.postgres_rows_select(connection,statement)
    html_table = build_html(html_tuple_list)
    return html_table

def send(resource,query,connection,messages=messages):
    statement = 'SELECT * FROM {0}'.format(messages[resource][query]['view'])
    html_table = build_message(connection,statement)
    email_result(messages[resource][query]['subject'],html_table)

def set_status_color(status):
    return {
        'In Progress': "Yellow",
        'Done': "Green",
        'Blocked': "Red"
    }.get(status)

def sprints_to_html_table(sprint_title , report_headers,report_data):
    html = '<html><head><style>h1 {color: green;text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}.tdErr {color:red;}.tdOk {color:green;}</style></head><body><h1></h1><table>'
    #build table headers
    html_headers = "<tr>"
    for header in report_headers:
        html_headers += "<th>{}</th>".format(header)
    html_headers += "</tr>"
    html += html_headers
    #build data
    for row in report_data:
        set_color = set_status_color(row[10])
        if set_color is not None:
            html_data = '<tr bgcolor="{0}">'.format(set_color)
        else:
            html_data = '<tr>'
        for field in row:
            html_data += "<td>{}</td>".format(field)
        html_data += "</tr>"
        html += html_data
    html += '</table></body></html>'
    return html

def email_sprints(connection,fields_list):
    statement = 'select * from vw_sprints_headers'
    sprints_headers = conn.postgres_rows_select(connection , statement)
    for sprint_header in sprints_headers:
        statement = "select * from vw_sprints_tot where sprint_title='{0}'".format(sprint_header[0])
        sprint_data = conn.postgres_rows_select(connection , statement)
        html = sprints_to_html_table(sprint_header[0],fields_list,sprint_data)
        subject = "Sprint '{0}' report - day {1} out of {2} days".format(sprint_header[0],sprint_header[4],sprint_header[3])
        email_result(subject, html)
