import os

from flask import Flask
from flask import current_app


app = Flask(__name__)


def get_env_variable(key):
    return current_app.config[key]


def set_env_variables(app: Flask):
    app.config["AMADEUS_API_KEY"] = os.getenv("AMADEUS_API_KEY", "KDzdGffAcDALOLdXrd1BK1xWP6LmUoro")
    app.config["AMADEUS_API_SECRET_KEY"] = os.getenv("AMADEUS_API_SECRET_KEY", "Ateg3JNMLLmVefig")
    app.config["AMADEUS_API_HOST"] = os.getenv("AMADEUS_API_HOST", "https://test.api.amadeus.com")
    app.config["AMADEUS_TOKEN_API_URI"] = os.getenv("AMADEUS_TOKEN_API_URI", "/v1/security/oauth2/token")
    app.config["AMADEUS_FLIGHT_OFFERS_API_URI"] = os.getenv("AMADEUS_FLIGHT_OFFERS_API_URI", "/v2/shopping/flight-offers")

    app.config["REDIS_HOST"] = os.getenv("REDIS_HOST", "localhost")
    app.config["REDIS_PORT"] = os.getenv("REDIS_HOST", "6379")
    app.config["REDIS_TTL"] = os.getenv("REDIS_TTL", "10000")
