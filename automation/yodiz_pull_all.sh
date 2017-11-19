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
    /usr/local/sqream-prerequisites/versions/system-default/bin/python2.7 ./yodiz.py pull -r $yodiz_resource -tr
    sleep 60
done

