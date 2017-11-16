from python.general_lib import fnx

def feedback_yodiz_issue_postgres():
    pass

def postgres_row_insert(connection ,row_dict):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Issues(Guid,Id,Title,UserStoryId,CreatedById,UpdatedOn,UpdatedById,CreatedOn,ResponsibleId,Status,Severity,ReleaseId,SprintId,EffortEstimate,EffortRemaining,EffortLogged) 
    values('{0}',{1},'{2}',{3},{4},'{5}',{6},'{7}',{8},'{9}','{10}',{11},{12},{13},{14},{15});
    """
    insert_statement = insert_statement_template.format(
        row_dict['Guid'], #{0} text
        row_dict['Id'], #{1} int
        fnx.escape_postgres_string(row_dict['Title']), #{2} text
        row_dict['UserStoryId'], #{3} int        
        row_dict['CreatedById'], #{4} int
        row_dict['UpdatedOn'], #{5} timestamp without time zone
        row_dict['UpdatedById'], #{6} int
        row_dict['CreatedOn'], #{7} timestamp without time zone
        row_dict['ResponsibleId'], #{8} int
        row_dict['Status'], #{9} text
        row_dict['Severity'], #{10} text
        row_dict['ReleaseId'], #{11} int
        row_dict['SprintId'], #{12} int
        row_dict['EffortEstimate'], #{13} real
        row_dict['EffortRemaining'], #{14} real
        row_dict['EffortLogged'] #{15} real
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()
    return feedback_yodiz_issue_postgres()