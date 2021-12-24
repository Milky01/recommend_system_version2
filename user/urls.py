from django.urls import path,re_path
from . import views
from templates import *

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('student_info/', views.student_info, name='student_info'),
    path('forget/',views.forget,name='forget'),
    re_path(r'^change/(.+)/$',views.change,name='change')
]
