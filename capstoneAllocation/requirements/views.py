from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Team


def index(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'requirements/login.html')

@login_required
def spaceRequest(request):
	team = Team.objects.get(teamID=team_id)
	return HttpResponse("{} request page".format(team))

@login_required
def confirmation(request, team_id):
	team = Team.objects.get(teamID=team_id)
	response = "confirmation page"
	return HttpResponse(response)

@login_required
def review(request, team_id):
	team = Team.objects.get(teamID=team_id)
	return HttpResponse("{} review page".format(team))