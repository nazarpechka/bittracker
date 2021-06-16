import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class API:
    def __init__(self, key, secret):
        self._key = key
        self._secret = secret

    @staticmethod
    def _request(url, headers=None, parameters=None):
        session = Session()
        if headers:
            session.headers.update(headers)

        data = None
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data

    def get_balance(self):
        raise NotImplementedError("get_balances() method isn't implemented!")
