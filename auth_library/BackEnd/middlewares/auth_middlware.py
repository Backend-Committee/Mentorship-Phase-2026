import jwt
from functools import wraps
from django.http import JsonResponse

def requireAuth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None
        
        if auth_header:
            parts = auth_header.split(' ')
            if len(parts) == 2:
                token = parts[1]

        if not token:
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        try:
            decoded = jwt.decode(token, 'secretkey', algorithms=["HS256"])
            request.user_info = decoded 
            return func(request, *args, **kwargs)

        except Exception as err:
            print('Token verification failed:', err)
            return JsonResponse({'message': 'Unauthorized'}, status=401)
            
    return wrapper