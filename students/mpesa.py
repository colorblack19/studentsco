import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

def get_access_token():
    if settings.MPESA_ENV == "live":
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    else:
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        )
    )

    # 👇 MUHIMU SANA (DEBUG)
    print("TOKEN STATUS:", response.status_code)
    print("TOKEN RAW TEXT:", response.text)

    # 👇 HII NDIO FIX YA ERROR YAKO
    if response.status_code != 200:
        raise Exception("M-PESA TOKEN ERROR")

    data = response.json()
    return data.get("access_token")



