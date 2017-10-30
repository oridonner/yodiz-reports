from python.general_lib import fnx

def feedback_yodiz_issue_postgres():
    pass

def postgres_row_insert(connection ,row_dict):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Releases(Guid,Id,Title,CreatedById,UpdatedOn,CreatedOn,Status,StartDate,EndDate) 
    values('{0}',{1},'{2}',{3},'{4}','{5}','{6}','{7}','{8}');
    """
    insert_statement = insert_statement_template.format(
        row_dict['Guid'], #{0} text
        row_dict['Id'], #{1} int
        fnx.escape_postgres_string(row_dict['Title']), #{2} text
        row_dict['CreatedById'], #{3} int
        row_dict['UpdatedOn'], #{4} timestamp without time zone
        row_dict['CreatedOn'], #{5} timestamp without time zone
        row_dict['Status'], #{6} text
        row_dict['StartDate'], #{7} timestamp without time zone
        row_dict['EndDate'] #{8} timestamp without time zone
        
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()
    return feedback_yodiz_issue_postgres()