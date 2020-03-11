from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Team
from . import form_input_checks


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

#@login_required
def spaceRequest(request):
<<<<<<< Updated upstream
	team = Team.objects.get(teamID=team_id)
	return HttpResponse("{} request page".format(team))
=======
	# team = Team.objects.get(teamID=team_id)
	#return HttpResponse("request page")
	return render(request, 'requirements/request.html')
>>>>>>> Stashed changes

#@login_required
def checkForm(request):
	#placeholder comment
	print(request.POST['representativeEmail'])
	print("This is the checkform request")
	print(request)

	return(render(request, 'requirements/request.html'))

#@login_required
def confirmation(request):
	
	#team = Team.objects.get(teamID=team_id)
	response = "confirmation page"
	return render(request, 'requirements/confirmation.html')

#@login_required
def review(request):
	#team = Team.objects.get(teamID=team_id)
	#return HttpResponse("{} review page".format(team))
	return render(request, 'requirements/review.html')