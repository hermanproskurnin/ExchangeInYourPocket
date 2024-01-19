import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'\nI don\'t convert the same currencies "{base}"'
                               f'\nYour request is illogical, isn\'t it?')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'\nUnfortunately, I am not familiar with the currency "{quote}" :(\n'
                               f'\nEnter the command\n/values to see the currencies I can convert.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'\nUnfortunately, I am not familiar with the currency "{base}" :(\n'
                               f'\nEnter the command\n/values to see the currencies I can convert.')

        try:
            amount = float(amount)

            if int(amount) > 0:
                amount = int(amount)
            else:
                raise APIException(f'\nThe amount cannot be negative: {amount}\n'
                                   f'\nPlease enter only positive values and use a dot as a decimal separator if necessary.')

        except ValueError:
            raise APIException(f'\nI could not process the entered amount: {amount}\n'
                               f'\nTake another look at what I can do\n/help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return float(total_base * amount)

class DeclensionByCases():
    def __init__(self, word, num):
        self.word = word
        self.num = num

    def incline(self):
        if self.word != 'euro':
            if (2 <= self.num % 10 <= 4 and self.num % 100 not in [12, 13, 14]) or not self.num.is_integer():
                return 'rubles' if self.word == 'ruble' else self.word + 's'
            if (self.num % 10 == 0 or 5 <= self.num % 10 <= 9 or 11 <= self.num % 100 <= 14) and self.num.is_integer():
                return 'rubles' if self.word == 'ruble' else self.word + 's'
        return self.word
