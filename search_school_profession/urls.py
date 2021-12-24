from django.urls import path, re_path
from . import views


urlpatterns = [
    path('search_school_profession/', views.search_school_profession, name='search_school_profession'),
]