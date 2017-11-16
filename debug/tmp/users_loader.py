from python.general_lib import fnx

def postgres_row_insert(connection ,row_dict):
    postgres_cursor = connection.cursor()
    insert_statement_template = """
    insert into Users(Id,FirstName,LastName,UpdatedOn,CreatedOn)
    values({0},'{1}','{2}','{3}','{4}');
    """
    insert_statement = insert_statement_template.format(
        row_dict['Id'], #{0} int
        row_dict['FirstName'], #{1} text
        row_dict['LastName'], #{2} text
        row_dict['UpdatedOn'], #{3} timestamp without time zone
        row_dict['CreatedOn'] #{4} timestamp without time zone
    ) 
    postgres_cursor.execute(insert_statement)
    connection.commit()

