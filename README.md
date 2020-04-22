# tayflutterwave
 A python library for easy 
 integration of flutterwave api into your applications
 
 ## Usage
 
 ### Pay With Card
 
 ```python
from tay_flutterwave import Flutterwave

secret_key = 'abcdefgh'
public_key = 'ijklmnop'

# Your Flutterwave Instance
# set live=False to use ravepay sandbox account, defaults to True
pay_object = Flutterwave(public_key, secret_key, live=False)



data = {
            "cardno": "2121212121", #Required
            "cvv": "123", #Required
            "expirymonth": "05", #Required
            "expiryyear": "21", #Required
            "currency": "NGN", #Default is NGN
            "country": "NG", #Required
            'suggested_auth': 'pin', 
            'pin': '2345',
            "amount": "100",
            'txRef': 'MC-TESTREF-1234',
            "email": "tay2druh@gmail.com", #Required
            "phonenumber": "07012345678",
            "firstname": "Abdulmateen",
            "lastname": "Tairu",
            "IP": "355426087298442",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }


pay_object.pay_via_card(data)
```

Check https://developer.flutterwave.com/reference#card-payments for 
data example.

After the process above, if 