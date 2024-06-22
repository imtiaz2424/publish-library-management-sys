from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from .models import Post, Order
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

# Create your views here.

# add post using class based view

@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('add_post')
    def form_valid(self, form):
        form.instance.users = self.request.user
        return super().form_valid(form)


# update post using class based view
@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')



# delete post using class based view
@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post   
    template_name = 'delete.html'   
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'



# @login_required
# def buy_now(request, id):
#     post = Post.objects.get(pk=id)
#     if post.quantity > 0:        
#         post.quantity -= 1
#         post.save()
#         order = Order(user=request.user, post=post)
#         order.save()
#         messages.success(request, 'Buy Successfully')
#         return redirect('profile')
#     else:
#         messages.warning(request, 'Out of Stock')
#         return redirect('profile')
    


    



class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=request.POST)
        
        post = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.post = post
            new_review.save()
            messages.success(request, 'Your review has been added.')
        else:
            messages.error(request, 'There was an error with your review.')
        return redirect('detail_post', id=post.id)         

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.comments.all()      
        review_form = forms.ReviewForm()
        
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context




