from modules.logger.logger import Logger
from modules.config.config import Config
from modules.database.database import Database

NAME = "web-operation-tool"

def run(logger):

	global LOGGER, CONFIG, DB
	if logger is None:
		from core import main
		BASE = "."
	else:
		from .core import main
		BASE = f"./modules/{NAME}"

	LOGGER = Logger(name=NAME)
	CONFIG = Config(path=f"{BASE}/config.ini").readConfig()
	DB = Database(LOGGER, CONFIG)

	LOGGER.info(f"Starting {CONFIG['VKore']['name']}")
	WOT = main.init(CONFIG, LOGGER, NAME, DB, BASE)
	LOGGER.info(f"Serving WOT on {CONFIG['Settings']['host']}:{CONFIG['Settings']['port']}")
	WOT.run(CONFIG['Settings']['host'], CONFIG['Settings']['port'])

# start up wot
if __name__ == '__main__':
	run(None)
