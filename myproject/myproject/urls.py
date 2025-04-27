"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from myapp import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    #anime関連
    path('anime/', views.anime_list, name='anime_list'),
    path('anime/<int:pk>/', views.anime_detail, name='anime_detail'),
    path('anime/form/', views.anime_form, name='anime_form'),
    path('anime/form/<int:pk>/', views.anime_form, name='anime_edit'),
    path('delete/<int:anime_id>/', views.anime_delete, name='anime_delete'),
    path('anime/search/', views.anime_search, name='anime_search'),
    #book関連
    path('book/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/form/', views.book_form, name='book_form'),
    path('book/form/<int:pk>/', views.book_form, name='book_edit'),
    path('delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path('book/search/', views.book_search, name = 'book_search'),
    #music関連
    path('music/', views.music_list, name='music_list'),
    path('music/<int:pk>/', views.music_detail, name = 'music_detail'),
    path('music/form/', views.music_form, name = 'music_form'),
    path('music/form/<int:pk>/', views.music_form, name = 'music_edit'),
    path('delete/<int:pk>/', views.music_form, name = 'music_delete'),  
    path('music/search/', views.music_search, name = 'music_search'),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
        ] + urlpatterns


