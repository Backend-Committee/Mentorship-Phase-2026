import json
import os
import jwt
import bcrypt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

User_DB = os.path.join(settings.BASE_DIR, 'BackEnd', 'DB', 'users.json')

@api_view(['POST'])
def register(request):
    try:
        data = request.data  
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not os.path.exists(User_DB):
            os.makedirs(os.path.dirname(User_DB), exist_ok=True)
            with open(User_DB, 'w') as f: json.dump([], f)
            
        with open(User_DB, 'r') as f:
            try: users = json.load(f)
            except: users = []
        
        userExists = next((u for u in users if u['email'] == email), None)
        
        if userExists:
            return JsonResponse({'message': 'User already exists'}, status=400)

        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        newUser = {
            'username': username,
            'email': email,
            'password': hashedPassword,
            'favorites': []
        }
        
        users.append(newUser)

        with open(User_DB, 'w') as f: json.dump(users, f, indent=2)

        return JsonResponse({
            'status': 'success',
            'message': 'User registered successfully',
            'user': {'username': username, 'email': email}
        }, status=201)

    except Exception as error:
        print("Register Error:", error)
        return JsonResponse({'message': 'Internal server error'}, status=500)


@api_view(['POST'])
def login(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not os.path.exists(User_DB): 
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
        
        with open(User_DB, 'r') as f: users = json.load(f)
        
        user = next((u for u in users if u['email'] == email), None)

        if not user:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

        isMatch = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))

        if not isMatch:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

        token = jwt.encode(
            {'id': user['email'], 'username': user['username']}, 
            'secretkey', 
            algorithm="HS256"
        )

        return JsonResponse({'message': 'Login successful', 'token': token}, status=200)

    except Exception as error:
        print("Login Error:", error)
        return JsonResponse({'message': 'Internal server error'}, status=500)