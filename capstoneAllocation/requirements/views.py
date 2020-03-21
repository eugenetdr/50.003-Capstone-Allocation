from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from .models import Team

prototype_size_dictionary = {"Small": [1,1,1], "Medium": [1.5,1.5,1.5], "Large": [2,2,2]}
showcase_size_dictionary = {"Small": [1.2,1.2,1.2], "Medium": [1.7,1.7,1.7], "Large":[2.2,2.2,2.2]}

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
		#return render(request, 'requirements/login.html', {"contextDict": default_context})
		return render(request, 'requirements/login.html')

#@login_required
def spaceRequest(request):
	#return HttpResponse("request page")
	return render(request, 'requirements/request.html')

#@login_required
def checkForm(request):
	keys = list((request.POST).keys())
	API_dict = {}

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
	text_inputs = ["representativeEmail", "projectName", "pedestalDescription", "others", "remarks"]
	for column in text_inputs:
		API_dict[column] = request.POST[column]
	for column in numerical_inputs:
		API_dict[column] = float(request.POST[column])
	print(API_dict)
	#Right now just reloads an empty form. 
	#TODO: Pass API_dict to backend API to store in database
	return render(request, 'requirements/confirmation.html')

#@login_required
def confirmation(request):
	#team = Team.objects.get(teamID=team_id)
	response = "confirmation page"
	return render(request, 'requirements/confirmation.html')

#@login_required
def review(request):
	#team = Team.objects.get(teamID=team_id)
	#return HttpResponse("{} review page".format(team))
	return render(request, 'requirements/review.html', {'prototypeType': '1:1', 'prototypeLength': 1, 'prototypeWidth': 1,\
	'prototypeHeight': 1, 'showcaseLength': 1, 'showcaseWidth': 1, 'showcaseHeight': 1, 'representativeEmail': 'rahulbhatta26@gmail.com',\
	'projectName': 'JavaProj', 'pedestalDescription': '3', 'others': 'None thank you', 'remarks': 'Thanks bro', 'powerpoints': 12.0,\
	'bigPedestals': 12.0, 'smallPedestals': 2.0, 'monitors': 4.0, 'TVs': 4.0, 'tables': 5.0, 'chairs': 6.0, 'HDMIAdaptors': 7.0})