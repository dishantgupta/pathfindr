from flask.views import View

from services.flight_offer_service import get_flights


class HealthController(View):

    methods = ["GET"]

    def dispatch_request(self):
        return {"data": "pong"}
