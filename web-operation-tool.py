from core import main

from modules.logger.logger import Logger
from modules.config.config import Config
from modules.database.database import Database

NAME = "web-operation-tool"
LOGGER = Logger(name=NAME)
CONFIG = Config(path="./config.ini").readConfig()
DB = Database(LOGGER, CONFIG)

# start up wot
if __name__ == '__main__':
	LOGGER.Info(f"Starting {CONFIG['VKore']['name']}")
	WOT = main.init(CONFIG, LOGGER, NAME, DB)
	LOGGER.Info(f"Serving WOT on {CONFIG['Settings']['host']}:{CONFIG['Settings']['port']}")
	WOT.run(CONFIG['Settings']['host'], CONFIG['Settings']['port'])
