import os
import sys
import email
import smtplib
from itertools import chain
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

def set_status_color(status):
    return {
        'In Progress': "Yellow",
        'Done': "Green",
        'Blocked': "Red"
    }.get(status)

def tot_report_to_HTML(tot_report_headers,tot_report_data):
    tot_html =  """
                        <div style="float: left;">
                            <table style="width: 30%">
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

def userstories_report_to_HTML(userstories_report_headers,userstories_report_data):
    userstory_html ="""
                        <table>
                            <tr>
                    """
    #build table header
    for header in userstories_report_headers[1:]:
        userstory_html +="""    <th>{}</th>
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

def issues_report_to_HTML(issues_report_headers,issues_report_data):
    issues_html ="""
                        <table>
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

def build_HTML(tot_report_headers,tot_report_data,userstories_report_headers,userstories_report_data,issues_report_headers,issues_report_data):
    #Open HTML
    html =  """
                    <html>
                        <head>
                            <style>h1 {color: black; font-weight:bold; text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}</style>
                        </head>
                            <body>
                                <h1>Daily Sprint Report</h1>
                                    <div style="display: inline-block">
            """
    #Build sprint total report HTML
    html += tot_report_to_HTML(tot_report_headers,tot_report_data)
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


    #Close HTML
    html += """
                            </body>
                    </html>
            """
    return html

#This function is exposed to API
def send(config,mailing_list,output_file):
    connection = conn.postgres_connect(config)
    report_rows = conn.get_rows_count(connection, 'vw_sprint_userstories_report')
    if report_rows > 0:
        statement = 'select * from vw_sprints_headers'
        sprints_headers = conn.get_rows(connection , statement)
        i=1
        for sprint_header in sprints_headers:
            userstories_report_headers = conn.get_table_culomns(connection,'vw_sprint_userstories_report')
            statement = "select * from vw_sprint_userstories_report where sprint_title='{0}'".format(sprint_header['sprint_title'])
            userstories_report_data = conn.postgres_rows_select(connection,statement)
            statement = "select * from vw_sprint_summary_report where sprint_title='{0}'".format(sprint_header['sprint_title'])
            tot_report_headers = conn.get_table_culomns(connection,'vw_sprint_summary_report')
            tot_report_data = conn.postgres_rows_select(connection,statement)
            statement = "select * from vw_sprint_issues_report where sprint_title='{0}'".format(sprint_header['sprint_title'])
            issues_report_headers = conn.get_table_culomns(connection,'vw_sprint_issues_report')
            issues_report_data = conn.postgres_rows_select(connection,statement)
            html = build_HTML(tot_report_headers,tot_report_data,userstories_report_headers,userstories_report_data,issues_report_headers,issues_report_data)
            if output_file:
                project_path = config['project']['path']
                html_lib = os.path.join(project_path,'.yodiz/debug/html/')
                html_file_name = os.path.join(html_lib,'sprints_{0}.html'.format(str(i)))
                html_file = open(html_file_name,"wb")
                html_file.writelines(html)
                html_file.close()
            else:
                subject = "Sprint '{0}' report - day {1} out of {2} days".format(sprint_header['sprint_title'],sprint_header['day_number'],sprint_header['total_days'])
                to_list = None
                cc_list = None
                if mailing_list:
                    if 'blue' in sprint_header['sprint_title'].lower():
                        to_list = config['mailing_list']['sprints']['blue']['to']
                        cc_list = config['mailing_list']['sprints']['blue']['cc']
                    if 'green' in sprint_header['sprint_title'].lower():
                        to_list = config['mailing_list']['sprints']['green']['to']
                        cc_list = config['mailing_list']['sprints']['green']['cc']
                fnx.send_email(subject,html,to_list,cc_list)
            i += 1