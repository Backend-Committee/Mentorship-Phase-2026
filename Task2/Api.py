import requests

res = requests.get('https://randomuser.me/api/')

print(res.status_code)
print(res.json())
gender = res.json()['results'][0]['gender']
first_name = res.json()['results'][0]['name']['first']
print(gender)
print(first_name)
print(f'{first_name} as {gender}')
