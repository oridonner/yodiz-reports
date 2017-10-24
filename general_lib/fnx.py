import email
import smtplib

def is_key_in_dictionary(d,n1,n2 = None,n3=None):
    if n1 not in d:
        return False
    if n2 is not None and n2 not in d[n1]:
        return False
    if n3 is not None and n3 not in d[n1][n2]:
        return False
    return True

def escape_postgres_string(string):
    return string.replace("'", "''")  

def postgres_rows_select(connection , statement):
    cur = connection.cursor()
    cur.execute(statement)
    connection.commit()    
    result = cur.fetchall()
    #html_list = [i[0] for i in html_tuple_list]
    #html = ' '.join(html_list)
    return result

# def email_result(html_table):
#     msg = email.mime.Multipart.MIMEMultipart()
#     body = email.mime.Text.MIMEText(html_table , 'html')
#     msg.attach(body)
#     msg['From']    = 'zbabira@sqreamtech.com'
#     msg['To'] = 'orid@sqreamtech.com'
#     msg['Subject'] = 'total open issues alert'
#     recips = 'orid@sqreamtech.com'
#     server = smtplib.SMTP('smtp.gmail.com')
#     server.starttls()
#     server.login('zbabira@gmail.com','sqreamzbabira')
#     server.sendmail('no-reply@sqreamtech.com', recips, msg.as_string())
#     server.quit()

