from flask.views import View
from flask import request, Response
from services.flight_offer_service import get_flights


class FlightController(View):
    methods = ["GET"]

    def dispatch_request(self):
        params = dict(request.args)
        return get_flights(params)
