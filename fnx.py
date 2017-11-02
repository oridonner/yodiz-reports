#!/usr/bin/env python2.7
import os 
import sys
import json
import yaml
import datetime
import operator
from python.yodiz_lib import pull
from python.yodiz_lib import mail
from python.postgres_lib.releases_lib import releases_mapper
from python.postgres_lib.releases_lib import releases_loader
from python.postgres_lib import postgres_connect as conn

def import_config():
    file_name = '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def main():

    config = import_config()
    connection = conn.postgres_connect(dbname=config['postgres']['dbname'],user=config['postgres']['user'],password=config['postgres']['password'],host=config['postgres']['host'],port=config['postgres']['port'])
    fields_list = conn.get_table_culomns(connection,'vw_userstories_tot')
    statement = 'select * from vw_userstories_tot'
    row_list = conn.postgres_rows_select(connection, statement)
    html = mail.sprints_to_html_table('test',fields_list,row_list)
    print html
    # html = """
    # <html>
    #     <head>
    #         <style>h1 {color: green;text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}.tdErr {color:red;}.tdOk {color:green;}</style>
    #     </head>
    #     <body>
    #         <h1></h1>
    #         <table>
    # """ 
    # html_headers = "<tr>"
    # for header in fields_list:
    #     html_headers += "<th>{}</th>".format(header)
    # html_headers += "</tr>"

    # html += html_headers
   

    # html_data =""
    # for row in row_list:
    #     html_data += "<tr>"
    #     for field in row:
    #         html_data += "<td>{}</td>".format(field)
    #     html_data += "</tr>"
    
    # html += html_data

    # html += """
    #         </table>
    #     </body>
    # </html>
    # """
    # print html
    
if __name__ == "__main__":
    main()
