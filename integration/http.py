
import requests


class HttpClient:

    @staticmethod
    def get(url, headers=None, query_params=None):
        resp = requests.get(url, headers=headers, params=query_params)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def post(url, body, headers=None, query_params=None):
        resp = requests.post(url, body, headers=headers, params=query_params)
        resp.raise_for_status()
        return resp.json()
