import os
import sys
import cgi
import email
import uuid
import smtplib
from itertools import chain
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header 
import sprint_chart as chart

def set_status_color(status):
    return {
        'In Progress': "Yellow",
        'Done': "Green",
        'Blocked': "Red"
    }.get(status)

def tot_report_to_HTML(sprint_title,connection):
    statement = "select * from vw_sprint_summary_report where sprint_title='{0}'".format(sprint_title)
    tot_report_headers = conn.get_table_culomns(connection,'vw_sprint_summary_report')
    tot_report_data = conn.postgres_rows_select(connection,statement)
    tot_html =  """
                        <div style="float: left;">
                            <table style="margin-top:12%; border-collapse:collapse; width:30%;">
                                <tr>
                """
    #build table header
    for header in tot_report_headers[1:]:
        tot_html +=                 """
                                        <th style='text-align: left;padding: 8px;background-color:black;color:white;'>{}</th>
                                    """.format(header)
    tot_html += """
                                </tr>
                """
    #build table data
    for row in tot_report_data:
        tot_html += """
                                <tr style="border-style:solid">
                    """
        #set second column id as hyperlink
        for field in row[1:]:
            tot_html +="""
                                    <td  style='padding:5px'>{}</td>
                        """.format(field)
        tot_html += """
                                </tr>
                    """
    tot_html += """
                            </table>
                        </div>
                """
    return tot_html

def embed_image_HTML(image_title,connection):
    cid=str(uuid.uuid4())
    image_html =MIMEText(
                """
                        <div dir="ltr" style="width:50%;float: right;">
                            <img src="cid:{0}" alt="{1}" style="max-width:80%;">
                        </div>
                """.format(cgi.escape(image_title, quote=True),cid), 'html', 'utf-8')           
    return image_html

def userstories_report_to_HTML(sprint_title,connection):
    userstories_report_headers = conn.get_table_culomns(connection,'vw_sprint_userstories_report')
    statement = "select * from vw_sprint_userstories_report where sprint_title='{0}'".format(sprint_title)
    userstories_report_data = conn.postgres_rows_select(connection,statement)
    userstory_html ="""
                        <table style="border-collapse: collapse;width: 100%;">
                            <tr>
                    """
    #build table header
    for header in userstories_report_headers[1:]:
        userstory_html +="""    <th style="background-color:#D9E9FF;">{}</th>
                         """.format(header)
    userstory_html += """
                            </tr>
                      """
    #build table data
    for row in userstories_report_data:
        set_color = set_status_color(row[3])
        if set_color is not None:
            userstory_html += """
                            <tr bgcolor="{0}" style="border-style:solid">
                        """.format(set_color)
        else:
            userstory_html += """
                            <tr style="border-style:solid">
                        """
        #set second column id as hyperlink
        link = 'https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-{0}'.format(row[1])
        userstory_html +="""
                                <td style='padding:5px'><a href='{0}' target='_blank'>{1}</a></td>
                         """.format(link,row[1])
        for i,field in enumerate(row[2:]):
            color = ""
            if (i == 3 and int(field) > 0):
                color = "color:red;font-weight:bold"
            userstory_html +="""
                                <td style='padding:5px'><span style="{1}">{0}</span></td>
                            """.format(field,color)
        userstory_html +="""
                            </tr>
                         """
    userstory_html += """
                        </table>
                      """
    return userstory_html

def issues_report_to_HTML(sprint_title,connection):
    statement = "select * from vw_sprint_issues_report where sprint_title='{0}'".format(sprint_title)
    issues_report_headers = conn.get_table_culomns(connection,'vw_sprint_issues_report')
    issues_report_data = conn.postgres_rows_select(connection,statement)
    issues_html ="""
                        <table style="border-collapse: collapse;width: 100%;">
                            <tr>
                    """
    #build table header
    for header in issues_report_headers[1:]:
        issues_html +="""    <th style="background-color:#C23F38;">{}</th>
                         """.format(header)
    issues_html += """
                            </tr>
                      """
    #build table data
    for row in issues_report_data:
        set_color = set_status_color(row[3])
        if set_color is not None:
            issues_html += """
                            <tr bgcolor="{0}" style="border-style:solid">
                        """.format(set_color)
        else:
            issues_html += """
                            <tr style="border-style:solid">
                        """
        #set second column id as hyperlink
        link = 'https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/bg-{0}'.format(row[1])
        issues_html +="""
                                <td style='padding:5px'><a href='{0}' target='_blank'>{1}</a></td>
                         """.format(link,row[1])
        for i,field in enumerate(row[2:]):
            #color = ""
            #if (i == 3 and int(field) > 0):
            #    color = "color:red;font-weight:bold"
            issues_html +="""
                                <td style='padding:5px'>{0}</td>
                            """.format(field)
        issues_html +="""
                            </tr>
                         """
    issues_html += """
                        </table>
                      """
    return issues_html

def build_HTML(tot_report_headers,tot_report_data,userstories_report_headers,userstories_report_data,issues_report_headers,issues_report_data,image_title):
    html =  """
                        <div style="width:75%;display: inline-block">
            """
    #Build sprint total report HTML
    html += tot_report_to_HTML(tot_report_headers,tot_report_data)
    #Build HTML to embed image
    html += embed_image_HTML(image_title)
    html += """
                        </div>
                        <br/>
                        <br/>
            """
    #Build sprint's userstories report HTML
    html += userstories_report_to_HTML(userstories_report_headers,userstories_report_data)
    html += """
                        <br/>
                        <br/>
        """
    #Build sprint's issues report HTML
    html += issues_report_to_HTML(issues_report_headers,issues_report_data)
    return html

def send_email_image(config,sprint_id,sprint_title,tot_report_html,userstories_report_html,issues_report_html,to_list=None,cc_list=None):
    if to_list is None:
        to_list = ['orid@sqreamtech.com']
    if cc_list is None:
        cc_list = ['orid@sqreamtech.com']
    recips_list = cc_list + to_list
    to_str = ','.join(to_list)
    cc_str = ','.join(cc_list)
    chart_path = config['project']['charts']
    chart_name = 'sprint_{0}.png'.format(str(sprint_id))
    chart_path_full = os.path.join(chart_path,chart_name)
    img = dict(title=chart_name, path=chart_path_full, cid=str(uuid.uuid4()),tot_report=tot_report_html,userstories_report=userstories_report_html,issues_report=issues_report_html )
    msg = MIMEMultipart('related')
    msg['From']    = 'zbabira@sqreamtech.com'
    msg['To'] = to_str
    msg['Cc'] = cc_str
    msg['Subject'] = sprint_title
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_text = MIMEText('[image: {title}]'.format(**img), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)

    msg_html = MIMEText("""
                        <div style="width:75%;display: inline-block">
                            {tot_report}
                            <div dir="ltr" style="width:50%;float: right;">
                                <img src="cid:{cid}" alt="{alt}" style="max-width:80%;">
                            </div>
                        </div>
                        <br/>
                        <br/>
                        {userstories_report}
                        <br/>
                        <br/>
                        {issues_report}
                        """.format(alt=cgi.escape(img['title'], quote=True), **img), 'html', 'utf-8')
    msg_alternative.attach(msg_html)

    with open(img['path'], 'rb') as file:
        msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
        msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))
        msg.attach(msg_image)

    #recips = "orid@sqreamtech.com"
    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login('zbabira@gmail.com','sqreamzbabira')
    s.sendmail('no-reply@sqreamtech.com', recips_list, msg.as_string())
    s.quit()

def create_sprint_chart(config,sprint_id):
    connection = conn.postgres_connect(config)
    statement = "select * from vw_sprint_burndown_chart where sprint_id ={0} order by sprint_day".format(sprint_id)
    #print statement
    sprint_chart_data = conn.get_rows(connection,statement)
    remaining_days = []
    trend_line = []
    remaining_effort = []
    for item in sprint_chart_data:
        remaining_days.append (item['remaining_days'])
        trend_line.append(item['trend_line'])
        remaining_effort.append(item['remaining_effort'])
    #print trend_line
    chart.build_sprint_chart(config,sprint_id, remaining_days,trend_line,remaining_effort)
  
#This function is exposed to API
def send(config,mailing_list,output_file):
    connection = conn.postgres_connect(config)
    report_rows = conn.get_rows_count(connection, 'vw_sprint_userstories_report')
    if report_rows > 0:
        statement = 'select * from vw_sprints_headers'
        sprints_headers = conn.get_rows(connection , statement)
        i=1
        for sprint_header in sprints_headers:
            sprint_id = sprint_header['sprint_id']
            sprint_title = sprint_header['sprint_title']
            html = ""# build_HTML(tot_report_headers,tot_report_data,userstories_report_headers,userstories_report_data,issues_report_headers,issues_report_data,image_title)
            tot_report_html = tot_report_to_HTML(sprint_title,connection)
            userstories_report_html = userstories_report_to_HTML(sprint_title,connection)
            issues_report_html = issues_report_to_HTML(sprint_title,connection)
            if output_file:
                project_path = config['project']['path']
                html_lib = os.path.join(project_path,'.yodiz/debug/html/')
                html_file_name = os.path.join(html_lib,'sprints_{0}.html'.format(str(i)))
                html_file = open(html_file_name,"wb")
                html_file.writelines(html)
                html_file.close()
            else:
                create_sprint_chart(config,sprint_id)
                subject = "Sprint '{0}' report - day {1} out of {2} days".format(sprint_header['sprint_title'],sprint_header['day_number'],sprint_header['total_days'])
                to_list = None
                cc_list = None
                if mailing_list:
                    if 'blue' in sprint_header['sprint_title'].lower():
                        to_list = config['mailing_list']['sprints']['blue']['to']
                        cc_list = config['mailing_list']['sprints']['blue']['cc']
                    if 'query engine' in sprint_header['sprint_title'].lower():
                        to_list = config['mailing_list']['sprints']['green']['to']
                        cc_list = config['mailing_list']['sprints']['green']['cc']
                send_email_image(config,sprint_id,sprint_title,tot_report_html,userstories_report_html,issues_report_html,to_list=to_list,cc_list=cc_list)
            i += 1