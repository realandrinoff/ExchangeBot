import math
import currencyapicom
import decimal
from decimal import getcontext, Decimal
from keys import currency_api

# Function that strips down all the currencies from useless data
# Checks if the entered data is in the dict
# Returns False, if it isnt, True, if it is
def check(currency):
    global client
    client = currencyapicom.Client(currency_api)
    allcurrencies = client.currencies().get("data")
    if currency in allcurrencies:
        return True
    else:
        return False
# The conversion and calculation of the result
# Imports data from currencyapi 
# Uses decimal for more accurate results
# Returns result
# Error handlers returns False if the result if bugged, or errored
def convert(amount, rate1, rate2):
    try:
        getcontext().prec = 999
        result = client.latest(rate1,currencies=[rate2])
        val1 = result.get('data')
        val2 = val1.get(rate2)
        val = val2.get("value")
        val = str(val)
        finalresult = Decimal(val) * Decimal(str(amount))
        finalresult = round(Decimal(finalresult), 2)
        int(finalresult)
        finalresult = str(finalresult)
        return finalresult
    except Exception as e:
        return e 