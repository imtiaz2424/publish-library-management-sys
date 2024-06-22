from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [   
   path('add/', views.AddPostCreateView.as_view(), name='add_post'),   
   path('edit/<int:id>/', views.EditPostView.as_view(), name='edit_post'),  
   path('delete/<int:id>/', views.DeletePostView.as_view(), name='delete_post'),
   path('details/<int:id>/', views.DetailPostView.as_view(), name='detail_post'),
   # path('buynow/<int:id>/', views.buy_now, name='buy_now'),  
     
]