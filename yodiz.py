#!/usr/bin/env python2.7
import os 
import sys
import yaml
from python.postgres_lib import postgres_connect as conn
from python.yodiz_lib import arg_parser
from python.yodiz_lib import pull
from python.yodiz_lib import mail

def import_config():
    file_name = '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def main():
    config = import_config()
    args = sys.argv
    params = arg_parser.params()
    
    connection = conn.postgres_connect(dbname=config['postgres']['dbname'],user=config['postgres']['user'],password=config['postgres']['password'],host=config['postgres']['host'],port=config['postgres']['port'])

    if args[1] == 'build':
        #print params
        if params['table'] :
            conn.create_table_objects(connection,params['table'])
        if params['show'] :
            conn.create_all_objects(connection,params['show'])
    if args[1] == 'pull':
        if ['resource'] :
            if params['truncate']:
                conn.truncate_table(connection,params['resource'])
            pull.load_resource(resource=params['resource'],api_key= params['key'],api_token= params['token'],connection=connection)
    if args[1] == 'mail':
        if params['issues'] :
            mail.send('issues',params['issues'][0],connection)
if __name__ == "__main__":
    main()
