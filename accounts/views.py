from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # Automatically log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Account created for {username} successfully!")
                return redirect('inventory:home_dashbord')
        
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {form: 'form'})