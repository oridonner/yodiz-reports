#!/bin/bash
LANG=en_GB.UTF-8 source $prerequisites_use;

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
    $prerequisites_python $yodiz_home"yodiz.py" pull -r $yodiz_resource -tr
    sleep 60
done

