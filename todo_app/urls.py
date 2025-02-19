from django.urls import path
from .views import Signup, Login, UpdatePassword

urlpatterns = [
    path('signup/', Signup.as_view(), name='Signup'),
    path('login/', Login.as_view(), name='Login'),
    path('update_password/', UpdatePassword.as_view(), name='UpdatePassword'),
]