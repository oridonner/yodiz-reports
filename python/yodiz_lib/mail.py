import sys
import email
import smtplib
from itertools import chain
#from python.general_lib import fnx
from python.postgres_lib import postgres_connect as conn
# psql named views are located in spcripts folder
# {"resource": "query":"postgres named vdiew"}

def get_report_view(report):
    reports={}
    reports['sprint tot']= 'vw_sprints_tot'
    reports['sprints']= 'vw_sprints_sub_tot'
    return reports[report]

# general send email function
def send_email(subject, html_table,to,cc=None):
    recips = cc + to
    msg = email.mime.Multipart.MIMEMultipart()
    body = email.mime.Text.MIMEText(html_table ,'html')
    for recip in recips:
        to = ','.join(recip)
        msg.attach(body)
        msg['From']    = 'zbabira@sqreamtech.com'
        msg['To'] = to
        msg['Subject'] = subject
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login('zbabira@gmail.com','sqreamzbabira')
        server.sendmail('no-reply@sqreamtech.com', recip, msg.as_string())
        server.quit()
        message = "email {0} successfully sent to: {1} cc: {2}".format(subject,to,cc)
        print message

# # general send email function
# def send_email(subject, html_table,to,cc=None):
#     msg = email.mime.Multipart.MIMEMultipart()
#     body = email.mime.Text.MIMEText(html_table ,'html')
#     recips = cc + to
#     if cc is not None:
#         cc = ','.join(cc)
#     else:
#         cc = ''
#     to = ','.join(to)
#     msg.attach(body)
#     msg['From']    = 'zbabira@sqreamtech.com'
#     msg['To'] = to
#     msg['Subject'] = subject
#     msg['Cc'] = cc
#     print recips
#     server = smtplib.SMTP('smtp.gmail.com')
#     server.starttls()
#     server.login('zbabira@gmail.com','sqreamzbabira')
#     server.sendmail('no-reply@sqreamtech.com', recips, msg.as_string())
#     server.quit()
#     message = "email {0} successfully sent to: {1} cc: {2}".format(subject,to,cc)
#     print message

def set_status_color(status):
    return {
        'In Progress': "Yellow",
        'Done': "Green",
        'Blocked': "Red"
    }.get(status)

def report_to_html_table(report_headers,report_data):
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

def email_sprints(connection,recips=None):
    report_rows = get_rows_count(connection, 'vw_sprints_sub_tot')
    if report_rows > 0:
        statement = 'select * from vw_sprints_headers'
        sprints_headers = conn.get_rows(connection , statement)
        for sprint_header in sprints_headers:
            view = get_report_view('sprints')
            statement = "select * from vw_sprints_sub_tot where sprint_title='{0}'".format(sprint_header['sprint_title'])
            report_data = conn.postgres_rows_select(connection,statement)
            report_headers = conn.get_table_culomns(connection,view)
            html = report_to_html_table(report_headers,report_data)
            subject = "Sprint '{0}' report - day {1} out of {2} days".format(sprint_header['sprint_title'],sprint_header['day_number'],sprint_header['total_days'])
            to = ['orid@sqreamtech.com','eliy@sqreamtech.com']
            send_email(subject,html,to=to,cc=recips)
