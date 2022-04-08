import utils
from godutch_db import connect_db
from godutch import run
from utils import *

if __name__ == '__main__':
    config, db_config, whitelist = utils.load_config()
    connect_db(db_config)
    run
