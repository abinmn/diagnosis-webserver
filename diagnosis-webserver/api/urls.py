from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api.views import *

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api-auth-token'), #To generate login token
    path('create-account/', UserCreate.as_view(), name='create-account'),
    path('user-profile/', UserProfile.as_view(), name='user-profilecls'),
    path('user-data/', UserData.as_view(), name='user-data'), #send data to android
    path('send-data/', SerialData.as_view(), name='send-data') #arduino
]
