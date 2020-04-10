from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from .models import Team, Request
from datetime import datetime
from pytz import timezone

prototype_size_dictionary = {"Small": [1,1,1], "Medium": [1.5,1.5,1.5], "Large": [2,2,2]}
showcase_size_dictionary = {"Small": [1.2,1.2,1.2], "Medium": [1.7,1.7,1.7], "Large":[2.2,2.2,2.2]}

def index(request):
	user = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			team = Team.objects.get(teamID=username)
			user=team.validate(password)
		except:
			return HttpResponse("Unknown User")
		if user==1:
			context = {'active': team.status, 'teamID': username, 'requestMade': team.requestMade}
			if team.requestMade:
				return redirect('review', team_id=username, active=team.status)
			else:
				return redirect('spaceRequest', team_id=username, active=team.status)
		elif user==0:
			return HttpResponse("Invalid login details given")
		else:
			team.logout()
			return HttpResponse("Multiple Logins Detected! Logging Out All Instances!")
	else:
		return render(request, 'requirements/login.html')


def spaceRequest(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	r = Request.objects.get(teamID=team_id)
	if (team.isLoggedIn()) & (active==1):
			
		if team.requestMade:
			context = {
			'teamID':team.teamID, 
			'active':team.status,
			'projectName':r.projectName,
			'prototypeType':r.pType,
			'representativeEmail':r.repEmail,
			'prototypeLength':r.pLength,
			'prototypeWidth':r.pWidth,
			'prototypeHeight':r.pHeight,
			'showcaseLength':r.sLength,
			'showcaseWidth':r.sWidth,
			'showcaseHeight':r.sHeight,
			'powerpoints':r.numPP,
			'bigPedestals':r.numBigPed,
			'smallPedestals':r.numSmallPed,
			'pedestalDescription':r.pedDesc,
			'monitors':r.numMonitor,
			'TVs':r.numTV,
			'tables':r.numTable,
			'chairs':r.numChair,
			'HDMIAdaptors':r.numHDMI,
			'others':r.other,
			}
			return render(request, 'requirements/editRequest.html',context)
		else:
			context = {
			'teamID':team.teamID, 
			'active':team.status}
			return render(request, 'requirements/request.html',context)
	else:
		return redirect('requirementIndex')

def checkForm(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	r = Request.objects.get(teamID=team_id)
	context = {'teamID':team.teamID, 'active':team.status}
	try:
		if (team.isLoggedIn()) & (active==1):
			if request.method == 'POST':
				keys = list((request.POST).keys())
				API_dict = {}
				print(request.POST["prototypeType"] == 'Custom Type')
				if(request.POST["prototypeType"] == 'Custom Type'):
					API_dict["prototypeType"] = request.POST["prototypeCustom"]
				else:
					API_dict["prototypeType"] = request.POST["prototypeType"]

				if(request.POST["prototypeSize"] == "OtherProtoSize"):
					API_dict["prototypeLength"] = float(request.POST["prototypeSize1"])
					API_dict["prototypeWidth"] = float(request.POST["prototypeSize2"])
					API_dict["prototypeHeight"] = float(request.POST["prototypeSize3"])
				else:
					protosize = prototype_size_dictionary[request.POST["prototypeSize"]]
					API_dict["prototypeLength"] = protosize[0]
					API_dict["prototypeWidth"] = protosize[1]
					API_dict["prototypeHeight"] = protosize[2]

				if(request.POST["showcaseSize"] == "OtherShowcaseSize"):
					API_dict["showcaseLength"] = float(request.POST["showcaseSize1"])
					API_dict["showcaseWidth"] = float(request.POST["showcaseSize2"])
					API_dict["showcaseHeight"] = float(request.POST["showcaseSize3"])
				else:
					showsize = prototype_size_dictionary[request.POST["showcaseSize"]]
					API_dict["showcaseLength"] = showsize[0]
					API_dict["showcaseWidth"] = showsize[1]
					API_dict["showcaseHeight"] = showsize[2]
				
				numerical_inputs = ["powerpoints", "bigPedestals", "smallPedestals", "monitors", "TVs", "tables", "chairs", "HDMIAdaptors"]
				text_inputs = ["representativeEmail", "projectName", "pedestalDescription", "others"]
				for column in text_inputs:
					API_dict[column] = request.POST[column]
				for column in numerical_inputs:
					API_dict[column] = float(request.POST[column])
				#example API_dict {'prototypeType': '1:1', 'prototypeLength': 1.5, 'prototypeWidth': 1.5, 'prototypeHeight': 1.5, 'showcaseLength': 1.5, 'showcaseWidth': 1.5, 'showcaseHeight': 1.5, 'representativeEmail': 'capstone1@capstone.com', 'projectName': 'capstone2020001', 'pedestalDescription': 'test', 'others': 'test', 'powerpoints': 0.0, 'bigPedestals': 0.0, 'smallPedestals': 1.0, 'monitors': 0.0, 'TVs': 0.0, 'tables': 1.0, 'chairs': 2.0, 'HDMIAdaptors': 1.0}
				#TODO: Pass API_dict to backend API to store in database
				API_dict['reqDateTime']=datetime.now()
				r.inputDetails(API_dict)
				team.madeRequest()
				return render(request, 'requirements/confirmation.html', context)
			else:
				return redirect('review')
		else:
			return redirect('requirementIndex')
	except:
		return render(request, 'requirements/failed_form_submit.html')


def confirmation(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	context = {'teamID':team.teamID, 'active':team.status}
	if (team.isLoggedIn()) & (active==1):
		return render(request, 'requirements/confirmation.html',context)
	else:
		return redirect('requirementIndex')


def review(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	r = Request.objects.get(teamID=team_id)
	context = {
		'teamID':team.teamID, 
		'active':team.status,
		'projectName':r.projectName,
		'prototypeType':r.pType,
		'representativeEmail':r.repEmail,
		'prototypeLength':r.pLength,
		'prototypeWidth':r.pWidth,
		'prototypeHeight':r.pHeight,
		'showcaseLength':r.sLength,
		'showcaseWidth':r.sWidth,
		'showcaseHeight':r.sHeight,
		'powerpoints':r.numPP,
		'bigPedestals':r.numBigPed,
		'smallPedestals':r.numSmallPed,
		'pedestalDescription':r.pedDesc,
		'monitors':r.numMonitor,
		'TVs':r.numTV,
		'tables':r.numTable,
		'chairs':r.numChair,
		'HDMIAdaptors':r.numHDMI,
		'others':r.other,
		}
	if (team.isLoggedIn()) & (active==1):
		return render(request, 'requirements/review.html',context)
	else:
		return redirect('requirementIndex')


def logout(request, team_id):
	team = Team.objects.get(teamID=team_id)
	team.logout()
	return redirect('requirementIndex')
