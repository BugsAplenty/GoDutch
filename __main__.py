import json
from GoDutch import GoDutch

config_file = open('config.json')
config = json.load(config_file)
token = config['token']

go_dutch_instance = GoDutch(token)

if __name__ == '__main__':
    go_dutch_instance.run()