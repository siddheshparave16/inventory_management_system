from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .views import register

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', success_url=reverse_lazy("{% url 'inventory:home-dashboard'%}")), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
