import logging

from flask import request
from flask.views import View

from services.flight_offer_service import get_flights

logger = logging.getLogger(__name__)


class FlightController(View):
    methods = ["GET"]

    def dispatch_request(self):
        params = dict(request.args)
        logger.debug("/flights/price api called: params: {}".format(params))
        resp = get_flights(params)
        logger.debug("/flights/price api success: params: {} resp: {}".format(params, resp))
        return resp
