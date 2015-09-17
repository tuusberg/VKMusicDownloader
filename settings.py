__author__ = 'Matthew Tuusberg'

import os
import json

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'config.json'), "r") as config_file:
    _data = config_file.read().replace('\n', '').replace('\t', '').replace('\r', '')
    GLOBAL_CONFIG = json.loads(_data)

email = GLOBAL_CONFIG['email']
password = GLOBAL_CONFIG['password']
app_id = GLOBAL_CONFIG['app_id']
output_folder = GLOBAL_CONFIG['output']
scope = "audio"
