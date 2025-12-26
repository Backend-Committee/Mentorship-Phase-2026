import requests as req
import json
import Auth

def retreive_Uni(data , uni_name):
    for item in data:
        if item['name'] == uni_name:
            print('found')
            print(f"University: {item['name']},\nCountry: {item['country']},\nWebsite: {item['web_pages']}")
            return
    print(f"No University found for {uni_name}")

with open("users.json", "a+") as file_obj:
    file_obj.seek(0)
    Auth.run_auth_system(file_obj)

endpoint = 'https://api.agify.io'
endpoint2 = 'http://universities.hipolabs.com/search'

name = input('Enter the country you search for: ')
params = {
    "country": name,
    "name": "technology"
}
try:
    response = req.get(endpoint2, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        University = input('Enter the name of University: ')
        retreive_Uni(data , University)

    else:
        print(f"Error: {response.status_code}")

except Exception as e:
    print(e)
