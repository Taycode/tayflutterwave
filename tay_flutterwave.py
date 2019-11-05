import hashlib
import requests
import json
import base64
from Crypto.Cipher import DES3


class Flutterwave(object):
    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a parameter"""

    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    @staticmethod
    def get_key(secret_key):
        hashed_secret_key = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashed_secret_key_last_12 = hashed_secret_key[-12:]
        secret_key_adjusted = secret_key.replace('FLWSECK-', '')
        secret_key_adjusted_first_12 = secret_key_adjusted[:12]
        return secret_key_adjusted_first_12 + hashed_secret_key_last_12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""
    @staticmethod
    def encrypt_data(key, plain_text):
        block_size = 8
        pad_diff = block_size - (len(plain_text) % block_size)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plain_text = "{}{}".format(plain_text, "".join(chr(pad_diff) * pad_diff))

        ''' 
        cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, 
        hence the need for the conversion below
        '''

        test = plain_text.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted

    def pay_via_card(self, data):

        data.update({'PBFPubKey': self.public_key})

        # hash the secret key with the get hashed key function
        hashed_sec_key = self.get_key(self.secret_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

        encrypt_key = self.encrypt_data(hashed_sec_key, json.dumps(data))

        # payment payload
        payload = {
            "PBFPubKey": self.public_key,
            "client": encrypt_key,
            "alg": "3DES-24"
        }

        # card charge endpoint
        endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/charge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

        return response.json()

    def validate_payment_with_card(self, transaction_reference, otp):
        data = {
            "PBFPubKey": self.public_key,
            "transaction_reference": transaction_reference,
            "otp": otp
        }
        endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/validatecharge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        return response.json()

    def transfer_to_bank(self, data):

        data.update({'seckey': self.secret_key})

        endpoint = "https://api.ravepay.co/v2/gpx/transfers/create"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        return response.json()

    def check_transfer_to_bank(self, reference):

        url = "https://api.ravepay.co/v2/gpx/transfers"

        querystring = {
            "seckey": self.secret_key,
            "reference": reference
        }

        headers = {'content-type': 'application/json'}

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()
