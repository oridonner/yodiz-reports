#!/usr/bin/env python2.7
import os 
import sys
import json
import datetime
from general_lib import arg_parser
from postgres_lib import postgres_connect as conn
from yodiz_lib import resources as yodiz
from yodiz_lib import message




def main():
    args = sys.argv
    params = arg_parser.params()
    
    postgres_host = '192.168.0.33'
    postgres_port = 5432
    postgers_user = 'postgres'
    postgres_password = 'postgres11'
    postgres_dbname = 'yodizdb'
    connection = conn.postgres_connect(postgres_dbname=postgres_dbname,postgers_user=postgers_user,postgres_password=postgres_password,postgres_host=postgres_host,postgres_port=postgres_port)

    if args[1] == 'pull':
        yodiz.load_resource(resource=params['resource'],api_key= params['key'],api_token= params['token'],connection=connection)
    if args[1] == 'mail':
        if params['issues'][0] == 'total':
                message.send('open',connection)
if __name__ == "__main__":
    main()