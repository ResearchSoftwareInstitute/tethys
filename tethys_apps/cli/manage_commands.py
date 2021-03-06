"""
********************************************************************************
* Name: manage_commands.py
* Author: Nathan Swain
* Created On: 2015
* Copyright: (c) Brigham Young University 2015
* License: BSD 2-Clause
********************************************************************************
"""

import os
import shutil
import subprocess

from tethys_apps.helpers import get_installed_tethys_apps

DEFAULT_INSTALLATION_DIRECTORY = '/usr/lib/tethys/src'
DEVELOPMENT_DIRECTORY = '/usr/lib/tethys/tethys'
MANAGE_START = 'start'
MANAGE_SYNCDB = 'syncdb'
MANAGE_COLLECTSTATIC = 'collectstatic'
MANAGE_COLLECTWORKSPACES = 'collectworkspaces'
MANAGE_COLLECT = 'collectall'
MANAGE_CREATESUPERUSER = 'createsuperuser'


def get_manage_path(args):
    """
    Validate user defined manage path, use default, or throw error
    """
    # Determine path to manage.py file
    manage_path = os.path.join(DEFAULT_INSTALLATION_DIRECTORY, 'manage.py')

    # Check for path option
    if args.manage:
        manage_path = args.manage

        # Throw error if path is not valid
        if not os.path.isfile(manage_path):
            print('ERROR: Can\'t open file "{0}", no such file.'.format(manage_path))
            exit(1)

    elif not os.path.isfile(manage_path):
        # Try the development path version
        manage_path = os.path.join(DEVELOPMENT_DIRECTORY, 'manage.py')

        # Throw error if default path is not valid
        if not os.path.isfile(manage_path):
            print('ERROR: Cannot find the "manage.py" file at the default location. Try using the "--manage"'
                  'option to provide the path to the location of the "manage.py" file.')
            exit(1)

    return manage_path


def manage_command(args):
    """
    Management commands.
    """
    # Get the path to manage.py
    manage_path = get_manage_path(args)

    # Define the process to be run
    primary_process = None

    if args.command == MANAGE_START:
        if args.port:
            primary_process = ['python', manage_path, 'runserver', args.port]
        else:
            primary_process = ['python', manage_path, 'runserver']
    elif args.command == MANAGE_SYNCDB:
        intermediate_process = ['python', manage_path, 'makemigrations']
        try:
            subprocess.call(intermediate_process)
        except KeyboardInterrupt:
            pass

        primary_process = ['python', manage_path, 'migrate']

    elif args.command == MANAGE_COLLECTSTATIC:
        # Run pre_collectstatic
        intermediate_process = ['python', manage_path, 'pre_collectstatic']
        try:
            subprocess.call(intermediate_process)
        except KeyboardInterrupt:
            pass

        # Setup for main collectstatic
        primary_process = ['python', manage_path, 'collectstatic']

    elif args.command == MANAGE_COLLECTWORKSPACES:
        # Run collectworkspaces command
        primary_process = ['python', manage_path, 'collectworkspaces']

    elif args.command == MANAGE_COLLECT:
        # Convenience command to run collectstatic and collectworkspaces
        ## Run pre_collectstatic
        intermediate_process = ['python', manage_path, 'pre_collectstatic']
        try:
            subprocess.call(intermediate_process)
        except KeyboardInterrupt:
            pass

        ## Setup for main collectstatic
        intermediate_process = ['python', manage_path, 'collectstatic']
        try:
            subprocess.call(intermediate_process)
        except KeyboardInterrupt:
            pass

        ## Run collectworkspaces command
        primary_process = ['python', manage_path, 'collectworkspaces']

    elif args.command == MANAGE_CREATESUPERUSER:
        primary_process = ['python', manage_path, 'createsuperuser']

    # Call the process with a little trick to ignore the keyboard interrupt error when it happens
    if primary_process:
        try:
            subprocess.call(primary_process)
        except KeyboardInterrupt:
            pass