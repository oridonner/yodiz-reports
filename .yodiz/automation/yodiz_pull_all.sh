#!/bin/bash
prereq_exec=$(./.yodiz/get_config_var.py "prerequisites.execute")
prereq_python=$(./.yodiz/get_config_var.py "prerequisites.python")
project_path=$(./.yodiz/get_config_var.py "project")

LANG=en_GB.UTF-8 source $prereq_exec;

yodiz_resources=(
    'users'
    'issues'
    'sprints'
    'userstories'
    'tasks'
    'releases'
)
#set -x
for yodiz_resource in ${yodiz_resources[@]};do
    $prereq_python $project_path pull -r $yodiz_resource -tr
    sleep 60
done

# send e-mail test reports 
$prereq_python $project_path mail --inv
$prereq_python $project_path mail --sprints 
$prereq_python $project_path mail --tasks
$prereq_python $project_path mail --release