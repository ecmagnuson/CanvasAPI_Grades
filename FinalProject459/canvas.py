import requests
import os 
import json

class CanvasRequests:
    # An object that has a modified get request for the API_URL, API_KEY,
    # headers, and the base url of the API_KEY in auth.json
    def __init__(self, extension_url = ""):
        self.extension_url = extension_url
        self.d = self.credentials()
        self.full_url = self.d["API_URL"] + self.extension_url

    def credentials(self):
        # Get the API_URL and API_KEY for canvas credentials
        auth = os.path.join(os.path.dirname(__file__), 'auth.json')
        with open(auth, "r") as f:
            d = json.load(f)
        return d

    def get(self, **kwargs):
        API_URL = self.d["API_URL"]
        API_KEY = self.d["API_KEY"]
        headers = {"Authorization": "Bearer " + API_KEY}
        return requests.get(self.full_url, headers=headers, params=kwargs)
