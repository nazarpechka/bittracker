from tracker.api.Binance import Binance


class APIFactory:
    @staticmethod
    def create(account):
        key = account.key
        secret = account.secret

        if account.exchange.name == "Binance":
            return Binance(key, secret)

        raise NotImplementedError(f"Exchange {account.exchange} is not yet supported!")