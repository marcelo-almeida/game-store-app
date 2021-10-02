from argparse import ArgumentParser
import os

APP_VERSION = '1.0.0'

parser = ArgumentParser()
parser.add_argument('-t', '--type', required=False, help='app, ddb', default='app')
args = parser.parse_args()

lines = []
with open('deploy/docker-compose-base.yaml') as file:
    for line in file:
        lines.append(line)
    template = ''.join(lines)
    with open('docker-compose.yaml', 'w') as f:
        f.write(template.format(version=APP_VERSION))

if args.type in ['app', 'ddb']:
    if args.type == 'app':
        os.system('docker build -t game-store:{} .'.format(APP_VERSION))
        os.system('docker-compose up -d app')
    else:
        os.system('docker-compose up -d dynamo')
    # {
    #     'app': lambda: (os.system('docker build -t game-store:{} .'.format(APP_VERSION)),
    #                     os.system('docker-compose up -d app')),
    #     'ddb': lambda: os.system('docker-compose up -d dynamo')
    # }.get(args.type, lambda: None)()
