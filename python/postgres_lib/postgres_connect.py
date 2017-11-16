import psycopg2
import datetime
from psycopg2.extras import RealDictCursor
import operator
import os

def postgres_connect(dbname,user,password,host,port):
    connection_string = "dbname={0} user={1} password={2} host={3} port={4}".format(dbname,user,password,host,port)
    connection = psycopg2.connect(connection_string)
    return connection

# outputs table columns by order
def get_table_culomns(connection,table_name):
    statement = """
        SELECT column_name,ordinal_position
        FROM information_schema.columns
        WHERE table_name   = '{0}'
    """.format(table_name)
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    
    fields = cur.fetchall()
    # insert imported data into dict {ordinal_position:column_name}
    fileds_dict = {}
    for field in fields:
        fileds_dict[field[1]]=field[0]   
    # sort imported columns by ordinal position
    fileds_dict_sorted = sorted(fileds_dict.items(), key=operator.itemgetter(0))
    fields_list=[]
    # get only column names
    for field in fileds_dict_sorted:
        fields_list.append(field[1])
    return fields_list

# this function returns rows from postgres db 
def postgres_rows_select(connection , statement):
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    
    result = cur.fetchall()
    return result

def get_rows(connection,statement):
    cur = connection.cursor(cursor_factory=RealDictCursor)
    cur.execute(statement)
    result = cur.fetchall()
    return result

def execute_statement(connection , statement):
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    

# this function truncates table in postgres
def truncate_table(connection, table_name):
    cur = connection.cursor()
    statement = 'truncate table {0}'.format(table_name)
    cur.execute(statement)
    print cur.query
    connection.commit()

def drop_table(connection, table_name):
    cur = connection.cursor()
    statement = 'drop table if exists {0} cascade'.format(table_name)
    cur.execute(statement)
    print cur.query
    connection.commit()

# this function truncates table inpostgres
def create_table(connection, table_name):
    cur = connection.cursor()
    file_name = 'tbl_{0}.sql'.format(table_name)
    file_path = os.path.join('postgres',table_name,file_name)
    print file_path
    cur.execute(open(file_path,'r').read())
    print cur.query
    connection.commit()

def create_table_objects(connection,table_name):
    cur = connection.cursor()
    file_name = '{0}_builder.sql'.format(table_name)
    file_path = os.path.join('postgres/build',file_name)
    print file_path
    cur.execute(open(file_path,'r').read())
    print cur.query
    connection.commit()

def update_userstory_issue(connection,issue_id,userstory_id):
    cur = connection.cursor()
    statement = 'update issues set userstoryid = {0} where id = {1}'.format(userstory_id,issue_id)
    cur.execute(statement)
    connection.commit()

def update_db_log(connection,transact_guid,table_name,rows_inserted):
    time_stamp = datetime.datetime.now()
    statement = "insert into db_log(transact_guid,table_name,rows_inserted,time_stamp) values('{0}','{1}',{2},'{3}')".format(transact_guid,table_name,rows_inserted,time_stamp)
    execute_statement(connection,statement)
    
def update_api_log(connection,transact_guid,http_req,response_code):
    time_stamp = datetime.datetime.now()
    statement = "insert into api_log(transact_guid,http_req,response_code,time_stamp) values('{0}','{1}',{2},'{3}')".format(transact_guid,http_req,response_code,time_stamp)
    execute_statement(connection,statement)
