import math
import currencyapicom
import decimal
from decimal import getcontext, Decimal

def convert(amount, rate1, rate2):
    try:
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
    except:
        error = "error"
        return error

        client = currencyapicom.Client('cur_live_b8rb8eMo1xzDTDdZDHdMEKh0dwy6YfmFYRDTFdHb')
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

# sfdjls;fjdsf
# convert(100, "RUB", "POP")