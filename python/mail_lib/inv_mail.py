import sys
import email
import smtplib
from itertools import chain
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

def report_to_html_table(report_headers,report_data):
    html = '<html><head><style>h1 {color: black; font-weight:bold; text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}</style></head><body><h1>Yodiz Data Validation Report</h1><table>'
    #build headers
    html_headers = "<tr>"
    for header in report_headers:
        html_headers += "<th>{}</th>".format(header)
    html_headers += "</tr>"
    #add headers to html
    html += html_headers
    #build data
    for row in report_data:
        html_data = '<tr style="border-style:solid">'
        for field in row:
            html_data += "<td>{}</td>".format(field)
        html_data += "</tr>"
        #add data to html
        html += html_data 
    #close html
    html += '</table></body></html>'
    return html

#This function is exposed to API
def send(config):
    connection = conn.postgres_connect(config)
    tasks_headers = conn.get_table_culomns(connection,'vw_inventory_tot')
    tasks_data = conn.postgres_rows_select(connection,'select * from vw_inventory_tot')
    html = report_to_html_table(tasks_headers,tasks_data)
    subject = "Yodiz Data Validation Report"
    to_list = None
    cc_list = None
    fnx.send_email(subject,html,to_list=to_list,cc_list=cc_list)