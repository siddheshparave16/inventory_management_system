from django.urls import path
from .views import dashbord

app_name = 'inventory'

urlpatterns = [
    path('', dashbord, name='home_dashboard'),
]
