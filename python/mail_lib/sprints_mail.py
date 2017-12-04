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
    for header in tot_report_headers[1:]:
        html_headers += "<th style='text-align: left;padding: 8px;background-color:black;color:white;'>{}</th>".format(header)
    html_headers += '</tr>'
    html += html_headers
    #build data
    for row in tot_report_data:
        html_data = '<tr style="border-style:solid">'
        #set second column id as hyperlink 
        for field in row[1:]:
            html_data += "<td  style='padding:5px'>{}</td>".format(field)
        html_data += '</tr>'
        html += html_data
    html += '</table></div>'
    return html

def sub_tot_report_to_html_table(sub_tot_report_headers,sub_tot_report_data):
    html = '<table>'    
    html_headers = "<tr>"
    for header in sub_tot_report_headers[1:]:
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
        link = 'https://app.yodiz.com/plan/pages/board.vz?cid=21431#/app/us-{0}'.format(row[1])
        html_data += "<td style='padding:5px'><a href='{0}' target='_blank'>{1}</a></td>".format(link,row[1])
        for field in row[2:]:
            html_data += "<td  style='padding:5px'>{}</td>".format(field)
        html_data += "</tr>"
        html += html_data 
    html += '</table>'
    return html

def report_to_html_doc(tot_report_headers,tot_report_data,sub_tot_report_headers,sub_tot_report_data):
    html = '<html><head><style>h1 {color: black; font-weight:bold; text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}</style></head><body><h1>Daily Sprint Report</h1>'
    html += '<div style="display: inline-block">'
    #build table headers
    tot_report_html_table = tot_report_to_html_table(tot_report_headers,tot_report_data)
    html += tot_report_html_table
    #html += '<div style="float: right;"><img src="http://192.168.0.55/yodiz/hurray.jpg" alt="hurray Icon"></img></div>'
    html += '</div><br/><br/>'
    sub_tot_report_html_table = sub_tot_report_to_html_table(sub_tot_report_headers,sub_tot_report_data)
    html += sub_tot_report_html_table
    html += '</body></html>'
    return html

#This function is exposed to API
def send(config,mailing_list):
    connection = conn.postgres_connect(config)
    report_rows = conn.get_rows_count(connection, 'vw_sprint_userstories_report')
    if report_rows > 0:
        statement = 'select * from vw_sprints_headers'
        sprints_headers = conn.get_rows(connection , statement)
        for sprint_header in sprints_headers:
            #view = get_report_view('sprints')
            statement = "select * from vw_sprint_userstories_report where sprint_title='{0}'".format(sprint_header['sprint_title'])
            sub_tot_report_data = conn.postgres_rows_select(connection,statement)
            sub_tot_report_headers = conn.get_table_culomns(connection,'vw_sprint_userstories_report')
            statement = "select * from vw_sprint_summary_report where sprint_title='{0}'".format(sprint_header['sprint_title'])
            tot_report_data = conn.postgres_rows_select(connection,statement)
            tot_report_headers = conn.get_table_culomns(connection,'vw_sprint_summary_report')            
            #html = report_to_html_table(report_headers,report_data)
            html = report_to_html_doc(tot_report_headers,tot_report_data,sub_tot_report_headers,sub_tot_report_data)
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