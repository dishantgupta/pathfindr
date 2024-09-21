import logging

from flask import Flask

from integration.amadeus import auth_token_cache
from url_register import health_url_register, app_url_register

logger = logging.getLogger(__name__)
logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ],
    format="[%(asctime)s] \t [%(levelname)s] \t %(name)s:  %(message)s",
    level=logging.DEBUG
)


def init_app():
    app = Flask(__name__, instance_relative_config=True)
    return app


if __name__ == '__main__':
    app = init_app()

    # populate token cache
    auth_token_cache.create_auth_token_cache()
    logger.debug("generated AMADEUS access token and refresh in cache")

    # register health URLs
    health_url_register.add_url(app)

    # register app URLs
    app_url_register.add_url(app)


    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
        load_dotenv=True
    )


