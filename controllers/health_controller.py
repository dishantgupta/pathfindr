import logging

from flask.views import View

logger = logging.getLogger(__name__)


class HealthController(View):

    methods = ["GET"]

    def dispatch_request(self):
        logger.debug("/flights/ping called: health check OK")
        return {"data": "pong"}
