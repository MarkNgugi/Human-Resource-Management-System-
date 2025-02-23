from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),    
    path('verify-otp/', verify_otp, name='verify_otp'),    
]
