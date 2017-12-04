#!/bin/bash
prereq_exec=$(./.yodiz/get_config_var.py "prerequisites.execute")
prereq_python=$(./.yodiz/get_config_var.py "prerequisites.python")
project_path=$(./.yodiz/get_config_var.py "project.path")
project_name=$(./.yodiz/get_config_var.py "project.name")
project=$project_path$project_name
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
    $prereq_python $project pull -r $yodiz_resource -tr
    sleep 60
done

# send e-mail test reports 
$prereq_python $project mail --inv
$prereq_python $project mail --sprints 
$prereq_python $project mail --tasks
$prereq_python $project mail --release