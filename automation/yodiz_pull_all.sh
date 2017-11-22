#!/bin/bash
LANG=en_GB.UTF-8 source /usr/local/sqream-prerequisites/versions/system-default/bin/use-prerequisites.sh;
yodiz_resources=(
    'users'
    'issues'
    'userstories'
    'tasks'
    'sprints'
    'releases'
)
#set -x
for yodiz_resource in ${yodiz_resources[@]};do
    # Productiom
    #/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/sqream/Documents/Yodiz/yodiz.py pull -r $yodiz_resource -tr
    
    # Dev\Test
    /usr/local/sqream-prerequisites/versions/3.04/bin/python /home/orid/Documents/projects/yodiz_new/yodiz.py pull -r $yodiz_resource -tr
    sleep 60
done

# send e-mail reports
# Production
/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/sqream/Documents/Yodiz/yodiz.py mail --sprints 
# Dev\Test
/usr/local/sqream-prerequisites/versions/3.04/bin/python /home/orid/Documents/projects/yodiz_new/yodiz.py mail --sprints 

