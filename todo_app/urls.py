from django.urls import path
from .views import Signup, Login, UpdatePassword, CreateTodo, ListTodos, UpdateTodo

urlpatterns = [
    path('signup/', Signup.as_view(), name='Signup'),
    path('login/', Login.as_view(), name='Login'),
    path('update_password/', UpdatePassword.as_view(), name='UpdatePassword'),
    path('todo/create/', CreateTodo.as_view(), name="CreateTodo"),
    path('todo/list/', ListTodos.as_view(), name="ListTodos"),
    path('todo/edit/<int:id>/', UpdateTodo.as_view(), name="UpdateTodo"),
]