from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashbord(request):
    return render(request, 'inventory/home.html')