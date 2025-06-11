"""Utility functions for interacting with the MPESA Daraja API."""
import base64
import json
import requests
from datetime import datetime
from django.conf import settings

class MPESAClient:
    def __init__(self):
        self.auth_url = settings.MPESA_AUTH_URL
        self.stk_url = settings.MPESA_STK_URL
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL

    def get_auth_token(self):
        """Get OAuth access token from Safaricom."""
        auth_string = base64.b64encode(
            f"{self.consumer_key}:{self.consumer_secret}".encode()
        ).decode()
        
        try:
            response = requests.get(
                self.auth_url,
                headers={"Authorization": f"Basic {auth_string}"}
            )
            response.raise_for_status()
            result = response.json()
            return result.get("access_token")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get auth token: {str(e)}")

    def initiate_stk_push(self, phone_number, amount):
        """Initiate STK Push transaction."""
        access_token = self.get_auth_token()
        if not access_token:
            raise Exception("Could not get access token")

        # Generate password and timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": "BAZAA",
            "TransactionDesc": "Monthly Budget Deposit"
        }

        try:
            response = requests.post(
                self.stk_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"STK push request failed: {str(e)}")
