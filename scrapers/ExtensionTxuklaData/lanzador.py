import webbrowser
import json
import os


with open("enlaces[1070].json", "r") as f:
    data = json.load(f)
    
    for i in range(0, len(data)):
        url = data[i]
        print(url)
    
    #webbrowser.open(url)
    
    
    



