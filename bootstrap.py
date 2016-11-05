#!/usr/bin/env python
# bootstrap.py

import os
import sys
import shutil
import subprocess
from optparse import OptionParser

from fabric.api import run, local, hosts, cd, prefix
from fabric.tasks import execute

import ConfigParser
import os

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'project.cfg'
configParser.read(configFilePath)

env_name = configParser.get('project-settings', 'env_name')
code_repo = configParser.get('repo-settings', 'repo_name')
path = configParser.get('project-path', 'env_path')
requirements_file = configParser.get('project-settings', 'requirements_file')

@hosts('127.0.0.1')
def main():
    if "VIRTUAL_ENV" not in os.environ:
        # Create virtual environment
        subprocess.call(["pip", "install", "virtualenv"])
        subprocess.call(["virtualenv", "--clear", "--distribute", (path + env_name)])
        # Move inside virtualenv and setup code
        with cd('%s%s/' % (path, env_name)):
            with prefix('source %s%s/bin/activate' % (path, env_name)):
                run('git clone %s' % code_repo)
                run('pip install -r %s' % requirements_file)
                #sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
                #parser.print_usage()
                #sys.exit(-1)

if __name__ == "__main__":
    execute(main)
    sys.exit(0)
