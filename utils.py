import json


def load_config():
    whitelist_file = open("whitelist.json")
    whitelist = json.load(whitelist_file)

    config_file = open("config.json")
    config = json.load(config_file)

    db_config_file = open("db_config.json")
    db_config = json.load(db_config_file)

    return config, db_config, whitelist
