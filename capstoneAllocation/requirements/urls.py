from django.urls import path

from . import views
from .models import Team

urlpatterns = [
	# ex: /requirements/
    path('', views.index, name='index'),
    # ex: /requirements/5/
    path('request/', views.spaceRequest, name='spaceRequest'),
    # ex: /requirements/5/confirmation/
    path('confirmation/', views.confirmation, name='confirmation'),
    # ex: /requirements/5/review/
    path('review/', views.review, name='review'),
    # ex: /requirements/5/review/
    #path('checkForm/', views.checkForm, name='checkForm')
    path('checkForm/', views.checkForm, name='checkForm')
]