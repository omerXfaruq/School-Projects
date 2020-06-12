import unittest
import json
import bitcoin_api

def isGetCoinRanksCorrect():
    response = bitcoin_api.getCoinRanks()

    if response is not None:
        if response["coins"] is not None:
            isCorrect = True
            for coin in response["coins"]:
                isCorrect = (isCorrect
                            and type(coin["rank"]) == int
                            and type(coin["symbol"]) == str
                            and type(coin["name"]) == str
                            and type(coin["price"]) == str
                            and type(coin["url"]) == str)

    return isCorrect


def isGetBitcoinPriceCorrect():
    response = bitcoin_api.getBitcoinPrice()

    currencies = ["EUR", "USD", "GBP"]
    attributes = ["code", "description", "rate", "rate_float", "symbol"]

    looks_right = (

        # CHECK IF THERE WAS A RESPONSE
        response

        # CHECK IF DISCLAIMER IS IN PLACE
        # AND OF THE CORRECT TYPE
        and response["disclaimer"]
        and type(response["disclaimer"]) == str

        # CHECK IF TIME UPDATED IS IN PLACE
        # AND OF THE CORRECT TYPE
        and response["time_updated"]
        and type(response["time_updated"]) == str

        # CHECK IF THE RATES ARE IN PLACE
        and response["rates"]
    )

    # IF SO FAR SO GOOD,
    # CHECK IF THE RETURNED JSON HAS ALL THREE CURRENCIES
    # AND ALL ATTRIBUTES THAT SHOULD EXIST FOR A CURRENCY
    if looks_right:
        for currency_key in currencies:
                if currency_key not in response["rates"]:
                    return False
                else:
                    for attribute in attributes:
                        if attribute not in response["rates"][currency_key]:
                            return False
        return True
    else:
        return False



class AltCoinTest(unittest.TestCase):

    # Returns True or False.
    def test(self):
        self.assertTrue(isGetCoinRanksCorrect() == True)

class BitcoinTest(unittest.TestCase):

    # Returns True or False.
    def test(self):
        self.assertTrue(isGetBitcoinPriceCorrect() == True)

if __name__ == '__main__':
    unittest.main()
