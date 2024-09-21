import logging
import os

from flask import Flask


logger = logging.getLogger(__name__)
logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ],
    format="[%(asctime)s] \t [%(levelname)s] \t %(name)s:  %(message)s",
    level=logging.DEBUG
)


def init_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


if __name__ == '__main__':
    app = init_app()

    # set config
    from config.env import set_env_variables
    set_env_variables()

    # populate token cache
    from integration.amadeus import auth_token_cache
    auth_token_cache.create_auth_token_cache()
    logger.debug("generated AMADEUS access token and refresh in cache")

    # register health URLs
    from url_register import health_url_register, app_url_register
    health_url_register.add_url(app)

    # register app URLs
    app_url_register.add_url(app)


    app.run(
        host='localhost',
        port=8080,
        debug=True,
        load_dotenv=True
    )


