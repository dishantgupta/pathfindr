from flask.views import View

from services.flight_offer_service import get_flights


class FlightController(View):
    methods = ["GET"]

    def dispatch_request(self):
        return get_flights()
