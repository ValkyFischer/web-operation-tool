from flask import Flask


NAME = None
LOGGER = None
CONFIG = None
DB_LINK = None
DB_CONN = None


def initBlueprints(app):
    from blueprints.auth import auth
    app.register_blueprint(auth)

    from blueprints.public import public
    app.register_blueprint(public)


def init(config, logger, name, db):

    global CONFIG, LOGGER, NAME
    LOGGER = logger
    CONFIG = config
    NAME = name

    WOT = Flask(NAME)
    WOT.config['SECRET_KEY'] = 'your-secret-key-goes-here'
    LOGGER.Info("Initialized Web Engine")

    global DB_LINK, DB_CONN
    DB_LINK, DB_CONN = db.connectMysql()
    LOGGER.Info("Initialized Database")

    initBlueprints(WOT)
    LOGGER.Info("Initialized Blueprints")

    return WOT
