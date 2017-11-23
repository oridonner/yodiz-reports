#!/bin/bash
LANG=en_GB.UTF-8 source /usr/local/sqream-prerequisites/versions/system-default/bin/use-prerequisites.sh;
# Dev\Test
#/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/orid/Documents/projects/yodiz_new/yodiz.py mail --sprints -ls @sprints_mailing_list.txt

# Production
#/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/sqream/Documents/Yodiz/yodiz.py mail --sprints -ls @sprints_mailing_list.txt
/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/sqream/Documents/Yodiz/yodiz.py mail --sprints 