from flask import Flask
import requests
import json

def getBitcoinPrice():

        url = "https://api.coindesk.com/v1/bpi/currentprice.json"

        response = requests.request("GET", url)

        result = response.json()

        json = {
            "rates":        result["bpi"],
            "disclaimer":   result["disclaimer"],
            "time_updated": result["time"]["updated"],
        }

        return json


def getCoinRanks():

        url = "https://api.coinranking.com/v1/public/coins"

        response = requests.request("GET", url)

        result = response.json()

        coinlist = [result["data"]["coins"][i] for i in range(10)]

        coinlist = [
            { 
              "rank": coin["rank"],
              "symbol": coin["symbol"],
              "name": coin["name"],
              "url": coin["websiteUrl"],
              "price": coin["price"]
            } 
         for coin in coinlist]

        json = {
            "coins" : coinlist
        }

        return json