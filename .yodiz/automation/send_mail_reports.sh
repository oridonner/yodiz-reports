#!/bin/bash
prereq_exec=$(./../get_config_var.py "prerequisites.execute")
prereq_python=$(./../get_config_var.py "prerequisites.python")
project_path=$(./../get_config_var.py "project")

LANG=en_GB.UTF-8 source $prereq_exec;

$prereq_python $project_path mail --inv -ls
$prereq_python $project_path mail --sprints -ls
$prereq_python $project_path mail --tasks -ls