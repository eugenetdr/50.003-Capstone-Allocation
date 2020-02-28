from django.shortcuts import render
from django.http import HttpResponse
from .models import Team


def index(request):
	return HttpResponse("Hello, world. You're at the login page.")

def spaceRequest(request, team_id):
	team = Team.objects.get(teamID=team_id)
	return HttpResponse("{} request page".format(team))

def confirmation(request, team_id):
	team = Team.objects.get(teamID=team_id)
	response = "confirmation page"
	return HttpResponse(response)

def review(request, team_id):
	team = Team.objects.get(teamID=team_id)
	return HttpResponse("{} review page".format(team))