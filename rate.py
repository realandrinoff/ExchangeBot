from currency_converter import CurrencyConverter
import math
import currencyapicom


def convert(amount, rate1, rate2):
    global finalresult
    amount = int(amount)
    client = currencyapicom.Client('cur_live_b8rb8eMo1xzDTDdZDHdMEKh0dwy6YfmFYRDTFdHb')
    result = client.latest(rate1,currencies=[rate2])
    print(result)
    print(type(result))
    val1 = result.get('data')
    print(val1)
    val2 = val1.get(rate2)
    print(val2)
    val = val2.get("value")
    print (val)
    print(type(val))
    print(val)
    print(amount)
    finalresult = val * amount
    print(finalresult)
    finalresult = math.ceil(finalresult)
    print(finalresult)
    return finalresult



# convert(100, "RUB", "POP")