from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import DbUser, Todo

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
        username = request.data.get('username')

        if not email or not password:
            return Response({"status": "400", "success":False, "error": True, "message": "Email e senha são necessários", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user:
            return Response({"status": "400", "success":False, "error": True, "message": "Usuário já está registrado no sistema", "data":None}, status=status.HTTP_400_BAD_REQUEST)
        
        
        new_user = User.objects.create(username=username, password=password, email=email)
        

        if not new_user:
            return Response({"status": "500", "success":False, "error": True, "message": "Erro interno no sistema", "data":None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_user.set_password(raw_password=password)
        new_user.save()

        tokens = get_tokens_for_user(user=new_user)

        novo_usuario = DbUser.objects.create(name=username, email=email)

        return Response({"status": "201", "success":True, "error": False, "message": "Sucesso", "data":{"user_id": novo_usuario.id, "tokens": tokens}}, status=status.HTTP_201_CREATED)

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password or not username:
            return Response({"status": "400", "success":False, "error": True, "message": "Email, senha e Nome de Usuário são necessários", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({"status": "400", "success":False, "error": True, "message": "Email, senha ou Nome de Usuário incorreto", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password) is False:
            return Response({"status": "400", "success":False, "error": True, "message": "Email, senha ou Nome de Usuário incorreto", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_tokens_for_user(user=user)

        dbuser = DbUser.objects.filter(email=email).first()

        return Response({"status": "200", "success":True, "error": False, "message": "Sucesso", "data":{"user_id": dbuser.id, "tokens": tokens}}, status=status.HTTP_200_OK)
    
class UpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"status": "400", "success":False, "error": True, "message": "Senha atual e futura são necessárias para atualizar", "data":None}, status=status.HTTP_400_BAD_REQUEST)
            
        if check_password(old_password, request.user.password) is False:
            return Response({"status": "400", "success":False, "error": True, "message": "Senha incorreta", "data":None}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({"status": "201", "success":True, "error": False, "message": "Senha atualizada com sucesso", "data":{"user_password": user.password}}, status=status.HTTP_201_CREATED)

class CreateTodo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        deadline = request.data.get('deadline')

        user = DbUser.objects.filter(email=request.user.email).first()

        if not title and description:
            return Response({"status": "400", "success":False, "error": True, "message": "É necessário título de descrição. ", "data":None}, status=status.HTTP_400_BAD_REQUEST)

        todo = Todo.objects.create(title=title, description=description, deadline=deadline, user=user)
        todo.save()

        return Response({"status": "201", "success": True, "error": False, "message": "Todo criado com sucesso. ", "data": {"title": todo.title, "description": todo.description, "created_at":todo.created_at}})