from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from .models import Team
from .form_input_checks import check_email, check_number, check_general_string, catch_no_input, prototype_size_dictionary, showcase_size_dictionary

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
	#return HttpResponse("request page")
	return render(request, 'requirements/request.html')

#@login_required
def checkForm(request):
	#print(request.POST["prototypeSize"])
	#placeholder comment
	#print(request.POST['representativeEmail'])
	#print("This is the checkform request")
	testresults = []

	print(check_number(1))

	#we can test all variables individually except for prototypeSize and showcaseSize. For these, we need to go deeper
	variables_functions = {'representativeEmail': check_email,'projectName': check_general_string,'prototypeType': check_general_string,'powerpoints': check_number,'bigPedestals':check_number,'smallPedestals':check_number,'pedestalDescription':check_general_string,'monitors':check_number,\
	'TVs':check_number,'tables':check_number,'chairs':check_number,'HDMIAdaptors':check_number, 'others':check_general_string}
	variables = list(variables_functions.keys())
	for var in variables:
		testresults.append(catch_no_input(variables_functions[var], request, var))
	#Now we need to check for prototypeSize and showcaseSize
	try:
		if(request.POST["prototypeSize"] == "otherProtoSize"):
			testresults.append(catch_no_input(check_number, request, "prototypeSize1"))
			testresults.append(catch_no_input(check_number, request, "prototypeSize2"))
			testresults.append(catch_no_input(check_number, request, "prototypeSize3"))
		else:
			try:
				prototypeSize = request.POST["prototypeSize"]
				size_array = prototype_size_dictionary[prototypeSize]
				testresults.append(check_number(size_array[0]))
				testresults.append(check_number(size_array[1]))
				testresults.append(check_number(size_array[2]))
			except KeyError:
				testresults.append(False)
				testresults.append(False)
				testresults.append(False)
	except MultiValueDictKeyError:
		testresults.append(False)
		testresults.append(False)
		testresults.append(False)
	
	try:
		if(request.POST["showcaseSize"] == "otherShowcaseSize"):
			testresults.append(catch_no_input(check_number, request, "showcaseSize1"))
			testresults.append(catch_no_input(check_number, request, "showcaseSize2"))
			testresults.append(catch_no_input(check_number, request, "showcaseSize3"))
		else:
			try:
				prototypeSize = request.POST["showcaseSize"]
				size_array = showcase_size_dictionary[prototypeSize]
				testresults.append(check_number(size_array[0]))
				testresults.append(check_number(size_array[1]))
				testresults.append(check_number(size_array[2]))
			except KeyError:
				testresults.append(False)
				testresults.append(False)
				testresults.append(False)
	except MultiValueDictKeyError:
		testresults.append(False)
		testresults.append(False)
		testresults.append(False)
	print(testresults)
	#comment for test
	return render(request, 'requirements/request.html')

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