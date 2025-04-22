from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
    path('hello/',views.hello, name='hello'), #this is the url for the hello function in views.py
]
