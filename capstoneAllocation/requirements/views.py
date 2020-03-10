from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Team


def validate(username, password):
	status = 0
	try:
		Team.objects.filter(teamID=username).get()
		team = Team.objects.get(teamID=username)
		if (password == team.teamPW) & (team.status==1):
			status=2
		elif (password == team.teamPW) & (team.status==0):
			status = 1
			team = Team.objects.get(teamID=username)
			team.status = 1
			team.save()
	except:
		status=0
	return status



def index(request):
	user = False
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = validate(username, password)
		if user==1:
			team = Team.objects.get(teamID=username)
			context = {'active': team.status, 'teamID': username, 'requestMade': team.requestMade}
			if team.requestMade:
				return redirect('review', team_id=username, active=team.status)
			else:
				return redirect('spaceRequest', team_id=username, active=team.status)
		elif user==0:
			return HttpResponse("Invalid login details given")
		else:
			return HttpResponse("Multiple Logins Detected!")
	else:
		return render(request, 'requirements/login.html')


def spaceRequest(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	if (active==team.status) & (active==1):
		context = {'teamID':team.teamID, 'active':team.status}
		return render(request, 'requirements/request.html',context)
	else:
		return redirect('requirementIndex')


def confirmation(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	context = {'teamID':team.teamID, 'active':team.status}
	if (active==team.status) & (active==1):
		team.requestMade = 1
		team.save()
		return render(request, 'requirements/confirmation.html',context)
	else:
		return redirect('requirementIndex')


def review(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	context = {'teamID':team.teamID, 'active':team.status}
	if (active==team.status) & (active==1):
		return render(request, 'requirements/review.html',context)
	else:
		return redirect('requirementIndex')


def logout(request, team_id):
	team = Team.objects.get(teamID=team_id)
	team.status=0
	team.save()
	return redirect('requirementIndex')