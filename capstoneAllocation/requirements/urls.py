from django.urls import path
from . import views
from .models import Team

urlpatterns = [
	# ex: /requirements/
    path('', views.index, name='requirementIndex'),
    # ex: /requirements/logout
    path('<int:team_id>/logout', views.logout, name='studentLogout'),
    # ex: /requirements/5/
    path('<int:team_id>/<int:active>/spaceRequest/', views.spaceRequest, name='spaceRequest'),
    # ex: /requirements/5/confirmation/
    path('<int:team_id>/<int:active>/confirmation/', views.confirmation, name='confirmation'),
    # ex: /requirements/5/review/
    path('<int:team_id>/<int:active>/review/', views.review, name='review'),
    path('<int:team_id>/<int:active>/checkForm/', views.checkForm, name='checkForm')
]