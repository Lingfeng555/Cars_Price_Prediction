import os
import json

with open('response.json', 'r') as f:
    data = json.load(f)
    print(len(data["items"]))
        