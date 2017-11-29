#!/usr/bin/env python2.7
import yaml
import sys
import os


def get_full_path(file):
    name = os.path.basename(file)
    full_path = os.path.abspath(file)
    path = full_path.split(name,1)[0]
    return path

def import_config(file):
    file_path = get_full_path(file)
    file_name = file_path + '.config'
    with open(file_name,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_yaml_var_path(var_path):
    var_path = var_path.split('.')
    yaml_var_path=''
    for item in var_path:
        yaml_var_path +="['" + item + "']"
    return yaml_var_path

def get_yaml_var(yaml_var_path,config):
    yaml_var = eval ('config{0}'.format(yaml_var_path))
    return yaml_var

def main ():
    var_path = sys.argv[1]
    yaml_var_path = get_yaml_var_path(var_path)
    config = import_config(__file__)
    yaml_var = get_yaml_var(yaml_var_path,config)
    print (yaml_var)
if __name__ == "__main__":
    main()