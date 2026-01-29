## let's make a random poem fetcher
# i want to fetch a random poem from an API and display it on my webpage
# We will use the PoetryDB API for this purpose
# random poem endpoint: https://poetrydb.org/random i only want one random poem, we will take the poem it self and store it in the output.json,
# then we will read from output.json and display it on the webpage
# each time the user refreshes the page, a new random poem should be fetched and displayed
# I want to make a list with all stored poems, we can press previous to get the previous poem and next to get the next poem
# If there is no previous poem, the previous button should be disabled
# if there is no next poem, the next button should be new poem, which fetches a new random poem from the API and adds it to the list
# that means we would make a counter index to keep track of which poem we are currently displaying
import requests
import json
import os

def load_previous():
    with open ("Database/output.json","r") as file:
        return json.load(file)
    
    
def save(data):
    with open ("Database/output.json", "w") as file:
        json.dump(data, file, indent=4)
 

def fetch_and_process():
    url = "https://poetrydb.org/random"
    
    while True:
        
        response = requests.get(url)
        data = response.json()

        if int(data[0]["linecount"]) <= 20:
            break
        
    poems = load_previous()


    newPoem = {
        # "id": len(poems["poems"]),
        # "id": max([poem["id"] for poem in poems["poems"]]) + 1 if poems["poems"] else 0,
        "id": max([poem["id"] for poem in poems["poems"]], default=-1) + 1,
        "title": data[0]["title"],
        "author": data[0]["author"],
        "lines": data[0]["lines"]
    }

    poems["poems"].append(newPoem)

    save(poems)

    return poems


def get_all_poems():
    poems = load_previous()
    return poems