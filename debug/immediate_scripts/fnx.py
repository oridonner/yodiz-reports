#!/usr/bin/env python2.7
import os 
import sys
import json
import datetime
from python.postgres_lib.issues_lib import issues_query 
from python.postgres_lib import postgres_connect as conn
from python.general_lib import fnx

def main():

    postgres_host = '192.168.0.33'
    postgres_port = 5432
    postgers_user = 'postgres'
    postgres_password = 'postgres11'
    postgres_dbname = 'yodizdb'
    connection = conn.postgres_connect(postgres_dbname=postgres_dbname,postgers_user=postgers_user,postgres_password=postgres_password,postgres_host=postgres_host,postgres_port=postgres_port)

    html_table = issues_query.get_total_open_issues(connection)
    fnx.email_result(html_table)
    #print fnx.postgres_rows_select(connection,'SELECT open_bugs from total_open_bugs;')[0][0]
if __name__ == "__main__":
    main()