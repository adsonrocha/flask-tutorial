import logging
import os
import sys


class Logger:
    """Simple singleton class to encapsulate logging to the Flask app object"""
    instance = None

    def __new__(cls, logger=None):
        if not Logger.instance:
            if not logger:
                raise ValueError("No logger specified on creation of Logger singleton.")
            Logger.instance = logger
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            return Logger.instance
        return Logger.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)


def log_http_error(response):
    """
    Private function to log errors on server console
    :param response: http response object.
    """
    if response.status_code == 403:
        Logger().error("Permission error, current scopes are - {}".format(os.environ['CLIMATE_API_SCOPES']))
    elif response.status_code == 400:
        Logger().error("Bad request - {}".format(response.text))
    elif response.status_code == 401:
        Logger().error("Unauthorized - {}".format(response.text))
    elif response.status_code == 404:
        Logger().error("Resource not found - {}".format(response.text))
    elif response.status_code == 416:
        Logger().error("Range Not Satisfiable - {}".format(response.text))
    elif response.status_code == 500:
        Logger().error("Internal server error - {}".format(response.text))
    elif response.status_code == 503:
        Logger().error("Server busy - {}".format(response.text))
