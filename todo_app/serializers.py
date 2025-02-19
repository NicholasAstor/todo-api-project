from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        
class ComentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'user', 'todo']
                
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'body', 'created_at', 'user', 'todo']
                
class TodocategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Todocategory
        fields = ['id', 'category', 'todo']        
        
class TodohistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Todohistory
        fields = ['id', 'changed_at', 'todo']
        
class DbUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbUser
        fields = ['id', 'name', 'email', 'created_at']
        
class UsercategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usercategory
        fields = ['id', 'user', 'category']
        