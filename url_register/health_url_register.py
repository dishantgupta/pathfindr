from flask import Flask

from controllers.health_controller import HealthController


def add_url(app: Flask):
    app.add_url_rule("/flights/ping", view_func=HealthController.as_view("check_health"))
