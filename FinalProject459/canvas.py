import requests
import os 
import json

class Canvas:
    # An object that has a modified get request for the API_URL, API_KEY,
    # headers, and the base url https://canvas.wisc.edu/api/v1/courses
    def __init__(self):
        self.d = self.credentials()
    
    def credentials(self):
        # Get the API_URL and API_KEY for canvas credentials
        auth = os.path.join(os.path.dirname(__file__), 'auth.json')
        with open(auth, "r") as f:
            d = json.load(f)
        return d

    def get(self, url = "", **kwargs):
        API_URL = self.d["API_URL"]
        API_KEY = self.d["API_KEY"]
        headers = {"Authorization": "Bearer " + API_KEY}
        full_url = API_URL + "/courses" + "/" + url
        return requests.get(full_url, headers=headers, params=kwargs)