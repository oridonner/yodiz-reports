#!/usr/bin/env python2.7
import os 
import sys
import json
import yaml

def get_mock_issues_data():
    mock_issues_data_file = 'mock_issues_data.json'
    with open(mock_issues_data_file,'r') as mock_file:
        mock_issues_data = yaml.safe_load(mock_file)
    return mock_issues_data

print get_mock_issues_data()[0]

