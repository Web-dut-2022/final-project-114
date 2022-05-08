"""Bookmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('books/', views.books, name='books'),
    path('authors/', views.authors, name='authors'),
    path('publish/', views.publish, name='publish'),
    path('borrow/', views.borrow, name='borrow'),

    path('add_book/', views.add_book, name='add_book'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_publish/', views.add_publish, name='add_publish'),
    re_path('edit_book/(\d+)', views.edit_book, name='edit_book'),
    re_path('del_book', views.del_book, name='del_book'),
    re_path('edit_author/(\d+)', views.edit_author, name='edit_author'),
    re_path('del_author', views.del_author, name='del_author'),
    re_path('edit_publish/(\d+)', views.edit_publish, name='edit_publish'),
    re_path('del_publish', views.del_publish, name='del_publish'),

    re_path('login/', views.login, name='login'),
    re_path('register/', views.register, name='register'),
    re_path('logout/', views.logout, name='logout'),

]
