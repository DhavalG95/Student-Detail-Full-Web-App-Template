from django.urls import path 
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('delete/<int:pk>',delete_student,name="delete_student"),
    path('add_student',add_student,name="add_student"),
    path('update_student/<int:pk>',update_student,name="update_student"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('add_data_template',add_data_template,name="add_data_template"),
    
]
