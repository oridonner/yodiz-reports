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

# post build psql script 
postgres_user=$(./.yodiz/get_config_var.py "postgres.user")
postgres_host=$(./.yodiz/get_config_var.py "postgres.host")
postgres_port=$(./.yodiz/get_config_var.py "postgres.port")
postgres_dbname=$(./.yodiz/get_config_var.py "postgres.dbname")
psql=$(./.yodiz/get_config_var.py "postgres.psql")

$psql -h $postgres_host -p $postgres_port -U $postgres_user -d $postgres_dbname -a -f .yodiz/build/post_build.sql


# send e-mail test reports 
$prereq_python $project mail --inv
$prereq_python $project mail --sprints 
$prereq_python $project mail --tasks
$prereq_python $project mail --release