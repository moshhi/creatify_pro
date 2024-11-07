from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password, check_password

# User = get_user_model()

# all user info 
users = {}


class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'msg': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        pwd= make_password(password)
        user_id = len(users) + 1
        user = {
            'id': user_id,
            'email': email,
            'password': pwd
        }
        users[email] = users.get(user_id, user)
        return Response({
            'userid': user_id,
            'email': email
        }, status=status.HTTP_200_OK)
    

class SigninView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'msg': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = users.get(email)

        if not user or not check_password(password, user['password']):
            return Response({'msg': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_obj = type('User', (object,), user)
        refresh = RefreshToken.for_user(user_obj)
        print('access token is:', str(refresh.access_token))
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)
    

class MeView(APIView):
    def get(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'msg': 'invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            access_token = AccessToken(token)
            email = access_token.payload.get('email')

            if not email:
                return Response({'msg': 'token does not contain email'}, status=status.HTTP_401_UNAUTHORIZED)

            user = users.get(email)
            if not user:
                return Response({'msg': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'id': user['id'],
                'email': user['email']
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'msg': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        