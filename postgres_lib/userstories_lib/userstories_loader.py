from general_lib import fnx

def feedback_yodiz_issue_postgres():
    pass

def postgres_row_insert(connection ,row_dict):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into UserStories(Guid,Id,Title,CreatedById,UpdatedOn,UpdatedById,CreatedOn,ResponsibleId,Status,ReleaseId,SprintId,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},'{2}',{3},'{4}',{5},'{6}',{7},'{8}',{9},{10},{11},{12},{13});
    """
    insert_statement = insert_statement_template.format(
        row_dict['Guid'], #{0} text
        row_dict['Id'], #{1} int
        fnx.escape_postgres_string(row_dict['Title']), #{2} text
        row_dict['CreatedById'], #{3} int
        row_dict['UpdatedOn'], #{4} timestamp without time zone
        row_dict['UpdatedById'], #{5} int
        row_dict['CreatedOn'], #{6} timestamp without time zone
        row_dict['ResponsibleId'], #{7} int - owner in yodiz api 
        row_dict['Status'], #{8} text
        row_dict['ReleaseId'], #{9} int
        row_dict['SprintId'], #{10} int
        row_dict['EffortEstimate'], #{11} real
        row_dict['EffortRemaining'], #{12} real
        row_dict['EffortLogged'], #{13} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()
    return feedback_yodiz_issue_postgres()