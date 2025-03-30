# app_config.py

import os
import sys

def get_app_root_path():
    '''Get the root path of the application, works in both dev and frozen states.'''
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Application paths
APP_ROOT = get_app_root_path()
CONFIG_PATH = os.path.join(APP_ROOT, 'folders_config.json')
