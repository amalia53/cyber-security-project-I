
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('userpage/<str:username>/', views.userpage, name='userpage'),
    path('post/', views.post, name='post'),
    path('delete/<int:bubble_id>/', views.delete_bubble, name='delete_bubble'),
    path('changepw/', views.changepw, name='changepw'),
]   