import os

APP_VERSION = '1.0.0'

lines = []
with open('docker-compose-base.yaml') as file:
    for line in file:
        lines.append(line)
    template = ''.join(lines)
    with open('docker-compose.yaml', 'w') as f:
        f.write(template.format(version=APP_VERSION))

os.system('docker build -t game-store:{} .'.format(APP_VERSION))
os.system('docker-compose up -d')
