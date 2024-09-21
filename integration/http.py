
import logging

import requests

from errors.exception import HttpException

logger = logging.getLogger(__name__)


class HttpClient:

    SUCCESS_STATUS_CODES = [200]

    @staticmethod
    def get(url, headers=None, query_params=None):
        resp = requests.get(url, headers=headers, params=query_params)
        if resp.status_code not in HttpClient.SUCCESS_STATUS_CODES:
            logger.error(
                "Request Failed: URL: {}, params: {}, headers: {}, Response: {}".format(
                    url, query_params, headers, resp.json())
            )
            raise HttpException(resp.json())
        return resp.json()

    @staticmethod
    def post(url, body, headers=None, query_params=None):
        resp = requests.post(url, body, headers=headers, params=query_params)
        if resp.status_code not in HttpClient.SUCCESS_STATUS_CODES:
            logger.error(
                "Request Failed: URL: {}, body: {}, headers: {}, Response: {}".format(
                    url, body, headers, resp.json())
            )
            raise HttpException(resp.json())
        return resp.json()
