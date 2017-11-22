import email
import smtplib
import os

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


def get_full_path(file):
    name = os.path.basename(file)
    full_path = os.path.abspath(file)
    path = full_path.split(name,1)[0]
    return path