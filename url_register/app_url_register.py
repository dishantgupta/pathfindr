from flask import Flask

from controllers.flight_controller import FlightController


def add_url(app: Flask):
    app.add_url_rule("/flights/price", view_func=FlightController.as_view("get_flights"))
