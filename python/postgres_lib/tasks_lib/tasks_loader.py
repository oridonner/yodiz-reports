from python.general_lib import fnx

def feedback_yodiz_issue_postgres():
    pass

def postgres_row_insert(connection ,row_dict):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Tasks(Guid,TaskId,UserStoryId,Title,CreatedById,UpdatedOn,UpdatedById,CreatedOn,Status,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},{2},'{3}',{4},'{5}',{6},'{7}','{8}',{9},{10},{11});
    """
    insert_statement = insert_statement_template.format(
        row_dict['Guid'], #{0} text
        row_dict['TaskId'], #{1} int
        row_dict['UserStoryId'], #{2} int
        fnx.escape_postgres_string(row_dict['Title']), #{3} text
        row_dict['CreatedById'], #{4} int
        row_dict['UpdatedOn'], #{5} timestamp without time zone
        row_dict['UpdatedById'], #{6} int
        row_dict['CreatedOn'], #{7} timestamp without time zone
        row_dict['Status'], #{8} text
        row_dict['EffortEstimate'], #{9} real
        row_dict['EffortRemaining'], #{10} real
        row_dict['EffortLogged'], #{11} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()
    return feedback_yodiz_issue_postgres()