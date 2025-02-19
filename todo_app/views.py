from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from .models import DbUser

# This function will return the serialized representation of the tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')

        if not email or not password:
            return Response({"status": "400", "success":False, "error": True, "message": "Email e senha são necessários", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user:
            return Response({"status": "400", "success":False, "error": True, "message": "Usuário já está registrado no sistema", "data":None}, status=status.HTTP_400_BAD_REQUEST)
        
        
        new_user = User.objects.create(username=name, password=password)
        

        if not new_user:
            return Response({"status": "500", "success":False, "error": True, "message": "Erro interno no sistema", "data":None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_user.set_password(raw_password=password)
        new_user.save()

        tokens = get_tokens_for_user(user=new_user)

        novo_usuario = DbUser.objects.create(name=name, email=email)

        return Response({"status": "201", "success":True, "error": False, "message": "Sucesso", "data":{"user_id": novo_usuario.id, "tokens": tokens}}, status=status.HTTP_201_CREATED)


