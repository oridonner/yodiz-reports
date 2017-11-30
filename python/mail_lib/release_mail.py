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

def tot_report_to_html_table(tot_report_headers,tot_report_data):
    html = '<div style="float: left;"><table style="width: 30%">'    
    html_headers = '<tr>'
    for header in tot_report_headers:
        html_headers += "<th style='text-align: left;padding: 8px;background-color:black;color:white;'>{}</th>".format(header)
    html_headers += '</tr>'
    html += html_headers
    #build data
    for row in tot_report_data:
        html_data = '<tr style="border-style:solid">'
        #set second column id as hyperlink 
        for field in row:
            html_data += "<td  style='padding:5px'>{}</td>".format(field)
        html_data += '</tr>'
        html += html_data
    html += '</table></div>'
    return html

def sub_tot_report_to_html_table(sub_tot_report_headers,sub_tot_report_data):
    html = '<table>'    
    html_headers = "<tr>"
    for header in sub_tot_report_headers:
        html_headers += "<th>{}</th>".format(header)
    html_headers += "</tr>"
    html += html_headers
    #build data
    for row in sub_tot_report_data:
        set_color = set_status_color(row[3])
        if set_color is not None:
            html_data = '<tr bgcolor="{0}" style="border-style:solid">'.format(set_color)
        else:
            html_data = '<tr style="border-style:solid">'
        #set second column id as hyperlink 
        for idx,field in enumerate(row):
            if idx == 1:
                link = 'https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-{0}'.format(row[1])
                html_data += "<td style='padding:5px'><a href='{0}' target='_blank'>{1}</a></td>".format(link,row[1])
            else:
                html_data += "<td  style='padding:5px'>{}</td>".format(field)
        html_data += "</tr>"
        html += html_data 
    html += '</table>'
    return html

def report_to_html_doc(tot_report_headers,tot_report_data,sub_tot_report_headers,sub_tot_report_data):
    html = '<html><head><style>h1 {color: black; font-weight:bold; text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}</style></head><body><h1>Daily Release Report</h1>'
    html += '<div style="display: inline-block">'
    #build table headers
    tot_report_html_table = tot_report_to_html_table(tot_report_headers,tot_report_data)
    html += tot_report_html_table
    html += '<div style="float: right;"><img src="http://192.168.0.55/yodiz/hurray.jpg" alt="hurray Icon"></img></div></div>'
    html += '<br/><br/>'
    sub_tot_report_html_table = sub_tot_report_to_html_table(sub_tot_report_headers,sub_tot_report_data)
    html += sub_tot_report_html_table
    html += '</body></html>'
    return html

#This function is exposed to API
def send(config,mailing_list):
    connection = conn.postgres_connect(config)
    report_rows = conn.get_rows_count(connection, 'vw_sprint_userstories_report')
    if report_rows > 0:
        # release headers for email subject
        release_headers = conn.get_rows(connection , "select * from vw_release_headers")[0]
        # release userstories fields and data
        sub_tot_report_data = conn.postgres_rows_select(connection,"select * from vw_release_userstories_report")
        sub_tot_report_headers = conn.get_table_culomns(connection,'vw_release_userstories_report')
        # release summary fields and data
        tot_report_data = conn.postgres_rows_select(connection,"select * from vw_release_summary_report")
        tot_report_headers = conn.get_table_culomns(connection,'vw_release_summary_report')            
        html = report_to_html_doc(tot_report_headers,tot_report_data,sub_tot_report_headers,sub_tot_report_data)
        subject = "Release '{0}' report - day {1} out of {2} days".format(release_headers['release_title'],release_headers['day_number'],release_headers['total_days'])
        to_list = None
        cc_list = None
        if mailing_list:
            to_list = config['mailing_list']['sprints']['to']
            cc_list = config['mailing_list']['sprints']['cc']
        fnx.send_email(subject,html,to_list,cc_list)
