from flask import Flask
from flask import cli

BASE = None
NAME = None
LOGGER = None
CONFIG = None
DB_LINK = None
DB_CONN = None


def initBlueprints(app):
    if BASE == ".":
        from blueprints.auth import auth
        app.register_blueprint(auth)
        from blueprints.public import public
        app.register_blueprint(public)

    else:
        from ..blueprints.auth import auth
        app.register_blueprint(auth)
        from ..blueprints.public import public
        app.register_blueprint(public)


def init(config, logger, name, db, base):
    cli.show_server_banner = lambda *_: None

    global CONFIG, LOGGER, NAME, BASE
    LOGGER = logger
    CONFIG = config
    NAME = name
    BASE = base

    WOT = Flask(
        import_name = f"{NAME}",
        template_folder = f"{BASE}/view",
        static_folder = f"{BASE}/static"
    )
    WOT.config['SECRET_KEY'] = 'your-secret-key-goes-here'
    LOGGER.info("Initialized Web Engine")

    global DB_LINK, DB_CONN
    DB_LINK, DB_CONN = db.connectMysql()
    LOGGER.info("Initialized Database")

    initBlueprints(WOT)
    LOGGER.info("Initialized Blueprints")

    return WOT
