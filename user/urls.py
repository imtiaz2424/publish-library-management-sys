from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserUpdateView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),      
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', UserUpdateView.as_view(), name='edit_profile'),
    path('profile/edit/pass_change/', views.pass_change, name='pass_change'),
]