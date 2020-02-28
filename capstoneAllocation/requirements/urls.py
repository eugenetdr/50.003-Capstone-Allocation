from django.urls import path

from . import views
from .models import Team

urlpatterns = [
	# ex: /requirements/
    path('', views.index, name='index'),
    # ex: /requirements/5/
    path('<int:team_id>/', views.spaceRequest, name='spaceRequest'),
    # ex: /requirements/5/confirmation/
    path('<int:team_id>/confirmation/', views.confirmation, name='confirmation'),
    # ex: /requirements/5/review/
    path('<int:team_id>/review/', views.review, name='review'),
]