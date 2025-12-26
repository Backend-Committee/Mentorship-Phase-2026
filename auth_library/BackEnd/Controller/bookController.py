import json
import os
import requests
import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

GUTENDEX_API_URL = 'https://gutendex.com/books/'
User_DB = os.path.join(settings.BASE_DIR, 'BackEnd', 'DB', 'users.json')

@api_view(['GET'])
def getRandomBook(request):
    try:
        response = requests.get(GUTENDEX_API_URL)
        books = response.json().get('results', [])
        if books:
            randomBook = random.choice(books)
            return JsonResponse(randomBook, safe=False)
        return JsonResponse({}, safe=False)
    except Exception as error:
        print('Error fetching random book:', error)
        return JsonResponse({'message': 'Error fetching random book'}, status=500)

@api_view(['GET'])
def getHighestBook(request):
    try:
        response = requests.get(GUTENDEX_API_URL)
        books = response.json().get('results', [])
        if books:
            highestBook = sorted(books, key=lambda x: x.get('download_count', 0), reverse=True)[0]
            return JsonResponse(highestBook, safe=False)
        return JsonResponse({}, safe=False)
    except Exception as error:
        print('Error fetching highest book:', error)
        return JsonResponse({'message': 'Error fetching highest book'}, status=500)

@api_view(['GET'])
def getOldestBook(request):
    try:
        response = requests.get(GUTENDEX_API_URL)
        books = response.json().get('results', [])
        def get_year(book):
            authors = book.get('authors', [])
            if authors and 'birth_year' in authors[0] and authors[0]['birth_year'] is not None:
                return authors[0]['birth_year']
            return 9999
        if books:
            oldestBook = sorted(books, key=get_year)[0]
            return JsonResponse(oldestBook, safe=False)
        return JsonResponse({}, safe=False)
    except Exception as error:
        print('Error fetching oldest book:', error)
        return JsonResponse({'message': 'Error fetching oldest book'}, status=500)

@api_view(['POST'])
def addFavoriteBook(request): 
    try:
        bookData = request.data
        
        userEmail = request.user_info['id']

        if not os.path.exists(User_DB):
            return JsonResponse({'message': 'Database error'}, status=500)

        with open(User_DB, 'r') as f:
            try: users = json.load(f)
            except: users = []
        
        user = next((u for u in users if u['email'] == userEmail), None)

        if not user:
            return JsonResponse({'message': 'User not found'}, status=404)

        if 'favorites' not in user: user['favorites'] = []

        isBookExists = next((b for b in user['favorites'] if b.get('id') == bookData.get('id')), None)
        
        if isBookExists:
            return JsonResponse({'message': 'Book already in favorites'}, status=400)

        user['favorites'].append(bookData)
        
        with open(User_DB, 'w') as f: json.dump(users, f, indent=2)

        return JsonResponse({'message': 'Book added to favorites successfully'}, status=200)

    except Exception as error:
        print('Error adding favorite:', error)
        return JsonResponse({'message': 'Internal server error'}, status=500)

@api_view(['GET'])
def getMyFavorites(request):
    try:
        userEmail = request.user_info['id']
        
        if not os.path.exists(User_DB): return JsonResponse([], safe=False)

        with open(User_DB, 'r') as f:
            try: users = json.load(f)
            except: users = []

        user = next((u for u in users if u['email'] == userEmail), None)

        if not user:
            return JsonResponse({'message': 'User not found'}, status=404)

        return JsonResponse(user.get('favorites', []), safe=False, status=200)

    except Exception as error:
        print('Error fetching favorites:', error)
        return JsonResponse({'message': 'Internal server error'}, status=500)