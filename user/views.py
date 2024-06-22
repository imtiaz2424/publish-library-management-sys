from django.shortcuts import render, redirect
from . import forms
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout, update_session_auth_hash 
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from posts.models import Post, Order
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

class UserRegistrationView(FormView):
    template_name = 'users/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')

    
def user_logout(request):
    logout(request)    
    return redirect('home')


@login_required
def profile(request):    
    orders = Order.objects.filter(user=request.user)  
    return render(request, 'users/profile.html', {'orders': orders}) 


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):
    template_name = 'users/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    


def pass_change(request):
    if request.method == 'POST':
        pass_change_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_change_form.is_valid():            
            messages.success(request, 'Password Updated Successfully')
            pass_change_form.save()
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('profile')
    else:
        pass_change_form = PasswordChangeForm(user=request.user)
    return render(request, 'users/pass_change.html', {'form' : pass_change_form})




    
    
    