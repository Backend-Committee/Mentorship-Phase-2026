import requests
import json
fetched_data = []
api_key = "QkXhBLUuoyaZtjEKo9BAlxjazAlA94kYYbxPfEKG"
for i in range (30):
    response = requests.get("https://api.api-ninjas.com/v1/quotes?", headers= {'X-Api-Key': api_key})
    if response.status_code == 200:
        fetched_data.append(response.json()[0])

with open('quotes.json', 'w') as o:
    json.dump(fetched_data, o, indent=4)

short_quotes = []
success_quotes = []
hope_quotes = []

for quote in fetched_data:
    if len(quote['quote']) < 100 :
        short_quotes.append({'category' : quote['category'],
                             'short_quote' : quote['quote'],
                             'author' : quote['author']})

    if quote['category'] == 'success':
        success_quotes.append({'success_quote' : quote['quote'],
                               'author' : quote['author']})

    if quote['category'] == 'hope':
        hope_quotes.append({'hape_quote' : quote['quote'],
                            'author' : quote['author']})

if len(short_quotes) > 0:
    with open('short_quotes.json', 'w') as o:
        json.dump(short_quotes, o, indent=4)
if len(success_quotes) > 0:
    with open('success_quotes.json', 'w') as o:
        json.dump(success_quotes, o, indent=4)
if len(hope_quotes) > 0:
    with open('hope_quotes.json', 'w') as o:
        json.dump(hope_quotes, o, indent=4)
