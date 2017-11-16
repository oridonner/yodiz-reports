#!/bin/bash
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
    ./yodiz.py pull -r $yodiz_resource -tr
    sleep 60
done

