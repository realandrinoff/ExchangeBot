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
    print(allcurrencies)
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
                

                print(result)
                print(type(result))
                val1 = result.get('data')
                print(val1)
                val2 = val1.get(rate2)
                print(val2)

                try:
                    val = val2.get("value")
                    print (val)
                    print(type(val))
                    print(val)
                    val = str(val)
                    print(amount)
                    finalresult = Decimal(val) * Decimal(str(amount))
                    finalresult = round(Decimal(finalresult), 2)
                    int(finalresult)
                    print ('went through 3')
                    print(finalresult)
                    finalresult = str(finalresult)
                    print(finalresult)
                    return finalresult
                except ValueError:
                    print(ValueError)
                    return False
            except Exception as e:
                print (e)
                return False 
