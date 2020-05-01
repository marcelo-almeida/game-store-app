import os
import argparse

APP_VERSION = '1.0.0'

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', required=False, help='all, ddb', default='all')
args = parser.parse_args()

lines = []
with open('docker-compose-base.yaml') as file:
    for line in file:
        lines.append(line)
    template = ''.join(lines)
    with open('docker-compose.yaml', 'w') as f:
        f.write(template.format(version=APP_VERSION))

if args.type in ['all', 'ddb']:
    if args.type == 'all':
        os.system('docker build -t game-store:{} .'.format(APP_VERSION))
        os.system('docker-compose up -d')
    else:
        os.system('docker-compose up -d dynamo')

