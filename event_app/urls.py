from django.urls import path
from . import views


urlpatterns =[
    path('event/',views.hello,name='hello'),
]
