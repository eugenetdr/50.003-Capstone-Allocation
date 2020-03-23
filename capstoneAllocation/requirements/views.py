from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from .models import Team, Request

prototype_size_dictionary = {"Small": [1,1,1], "Medium": [1.5,1.5,1.5], "Large": [2,2,2]}
showcase_size_dictionary = {"Small": [1.2,1.2,1.2], "Medium": [1.7,1.7,1.7], "Large":[2.2,2.2,2.2]}

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
		#return render(request, 'requirements/login.html', {"contextDict": default_context})
		return render(request, 'requirements/login.html')


def spaceRequest(request, team_id, active):
	team = Team.objects.get(teamID=team_id)
	r = Request.objects.get(teamID=team_id)
	if (active==team.status) & (active==1):
			
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
	if (active==team.status) & (active==1):
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
			#Right now just reloads an empty form. 
			#TODO: Pass API_dict to backend API to store in database
			r=Request(
				r.pk,
				teamID=team_id, 
				pType=API_dict['prototypeType'],
				pLength=API_dict['prototypeLength'],
				pWidth=API_dict['prototypeWidth'],
				pHeight=API_dict['prototypeHeight'],
				sLength=API_dict['showcaseLength'],
				sWidth=API_dict['showcaseWidth'],
				sHeight=API_dict['showcaseHeight'],
				repEmail=API_dict['representativeEmail'],
				projectName=API_dict['projectName'],
				pedDesc=API_dict['pedestalDescription'],
				other=API_dict['others'],
				numPP=API_dict['powerpoints'],
				numBigPed=API_dict['bigPedestals'],
				numSmallPed=API_dict['smallPedestals'],
				numMonitor=API_dict['monitors'],
				numTV=API_dict['TVs'],
				numTable=API_dict['tables'],
				numChair=API_dict['chairs'],
				numHDMI=API_dict['HDMIAdaptors'])
			r.save()
			team.requestMade = 1
			team.save()
			return render(request, 'requirements/confirmation.html', context)
		else:
			return redirect('review')
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
	if (active==team.status) & (active==1):
		return render(request, 'requirements/review.html',context)
	else:
		return redirect('requirementIndex')


def logout(request, team_id):
	team = Team.objects.get(teamID=team_id)
	team.status=0
	team.save()
	return redirect('requirementIndex')