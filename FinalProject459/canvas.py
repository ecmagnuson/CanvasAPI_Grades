import requests
import os 
import json

from main import credentials

class Courses:
    def __init__(self):
        self.d = credentials()
    
    @classmethod 
    def credentials(cls):
        # Get the API_URL and API_KEY for canvas credentials
        auth = os.path.join(os.path.dirname(__file__), 'auth.json')
        with open(auth, "r") as f:
            d = json.load(f)
        return d

    def get(self, url = "", **kwargs):
        headers = {"Authorization": "Bearer " + self.d["API_KEY"]}
        full_url = self.d["API_URL"] + "/courses" + "/" + url
        return requests.get(full_url, headers=headers, params=kwargs)

c = Courses()
params = { #API https://canvas.instructure.com/doc/api/courses.html
            "enrollment_type": "teacher", 
            "enrollment_state": "active", 
            #"include": ["sections"]
        }   

courses = c.get(**params).json()

for c in courses:
    print(c["name"])
    print()

