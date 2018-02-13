import sys
import email
import smtplib
from itertools import chain
from python.general_lib import fnx
from python.general_lib import postgres_connect as conn

def set_status_color(status):
    return {
        'Overload': "Red",
        'Idle': "Orange",
        'OK': None
    }.get(status)

def unassigned_report_to_HTML(unassigned_report_data):
    unassigned_html =          """
                        <div style="float: left;">
                            <table style="width: 100%">
                    """    
    unassigned_html +=         """
                                <tr><th style='text-align: left;padding: 8px;background-color:black;color:white;'>Unassigned Developers</th></tr>
                    """
    #build data
    for row in unassigned_report_data:
        unassigned_html +=     """
                                <tr style="border-style:solid"><td  style='padding:5px'>{}</td></tr>
                    """.format(row[0])
    unassigned_html +=         """
                            </table>
                            <br/><br/><br/><br/>
                        </div>
                    """
    return unassigned_html


def capacity_report_to_HTML(capacity_report_headers,capacity_report_data):
    #build report table headers
    #----------------------
    capacity_html =  """
                        <div>
                            <table>
                                <tr>
                    """
    for header in capacity_report_headers:
        capacity_html +=    """
                                    <th>{}</th>
                            """.format(header)
                                        
    capacity_html +=        """
                                </tr>
                            """
    
    #build report table data
    #-----------------------
    for row in capacity_report_data:
        set_color = set_status_color(row[8])
        if set_color is not None:
            capacity_html +="""
                                <tr bgcolor="{0}" style="border-style:solid">
                            """.format(set_color)
        else:
            capacity_html +="""
                                <tr style="border-style:solid">
                            """
        for field in row:
            capacity_html +="""
                                    <td>{}</td>
                            """.format(field)
        capacity_html +=    """
                                </tr>
                            """
    capacity_html += """
                            </table>
                        </div>
                    """
    return capacity_html


def build_HTML(capacity_report_headers,capacity_report_data,unassigned_report_data):
    #Open HTML
    html =  """ 
                <html>
                    <head>
                        <style>h1 {color: black; font-weight:bold; text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}</style>
                    </head>
                    <body>
                        <h1>Daily Capacity Report</h1>
            """
    
    #Build unassigned report HTML
    html += unassigned_report_to_HTML(unassigned_report_data)
    #Build capacity report HTML
    html += capacity_report_to_HTML(capacity_report_headers,capacity_report_data)
    
    #close HTML
    html += """
                    </body>
                </html>
            """
    return html

#This function is exposed to API
def send(config,mailing_list,output_file):
    connection = conn.postgres_connect(config)
    unassigned_report_data = conn.postgres_rows_select(connection,'select full_name from vw_capacity_unassigned')
    capacity_report_headers = conn.get_table_culomns(connection,'vw_capacity_report')
    capacity_report_data = conn.postgres_rows_select(connection,'select * from vw_capacity_report where "Sprint Title" is not null')
    html = build_HTML(capacity_report_headers,capacity_report_data,unassigned_report_data)
    if output_file:
        print output_file
    else:
        subject = "R&D members - Sprint capacity report"
        to_list = None
        cc_list = None
        if mailing_list:
            to_list = config['mailing_list']['capacity']['to']
            cc_list = config['mailing_list']['capacity']['cc']
        fnx.send_email(subject,html,to_list=to_list,cc_list=cc_list)