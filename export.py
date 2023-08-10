#!/usr/bin/env python

"""
This script exports all the devices from a TTS Application and creates a 
CSV file that can be imported back into a TTS Application. The script is
useful for moving devices between Things Applications or Accounts.

The "ttn-lw-cli" command line utility must be installed.Also, you must
use the command "ttn-lw-cli login" to authorize the TTN CLI
before using this script.  You can also login without a browser by using
   ttn-lw-cli login --api-key <API Key from Application>

Usage:
   ./export.py <Application ID to export> <output CSV file name>
ID of the TTS Application that you want to export.
"""
import subprocess
import sys
import json

app_id = sys.argv[1]
out_file = sys.argv[2]

command = [
    'ttn-lw-cli', 'device', 'list', app_id, 
    '--version-ids', '--description', '--name',
]
result = subprocess.run(command, stdout=subprocess.PIPE)

# create a list of devices, each device being a dictionary
devices = json.loads(result.stdout.decode())

# Create a CSV file that can be imported into a Things Application
with open(out_file, 'w') as fout:
    field_names = [
        'id',
        'dev_eui',
        'join_eui',
        'app_key',
        'name',
        'description',
        'lorawan_version',
        'lorawan_phy_version',
        'frequency_plan_id',
        'brand_id',
        'model_id',
        'firmware_version',
        'hardware_version',
        'band_id'
    ]
    print(';'.join(field_names), file=fout)

    for d in devices:
        dev_id = d['ids']['device_id']
        print(dev_id)
        command =  [
            'ttn-lw-cli', 'device', 'get', app_id, dev_id, 
            '--root-keys.app-key.key', '--frequency-plan-id', 
            '--lorawan-version', '--lorawan-phy-version'
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        dev = json.loads(result.stdout.decode())
        values = [
            dev_id,
            d['ids']['dev_eui'],
            d['ids']['join_eui'],
            dev['root_keys']['app_key']['key'],
            d.get('name', ''),
            d.get('description', ''),
            dev['lorawan_version'],
            dev['lorawan_phy_version'],
            dev['frequency_plan_id'],
            d['version_ids'].get('brand_id', ''),
            d['version_ids'].get('model_id', ''),
            d['version_ids'].get('firmware_version', ''),
            d['version_ids'].get('hardware_version', ''),
            d['version_ids'].get('band_id', ''),
        ]
        print(';'.join(values), file=fout)

