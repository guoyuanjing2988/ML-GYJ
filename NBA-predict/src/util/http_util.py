import requests

def readContentFromURL(url):
    r=requests.get(url)
    return r.text.strip()