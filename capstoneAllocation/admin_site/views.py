# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admin
from requirements.models import Team, Request
import json

# Create your views here.

def validate(username, password):
	status = 0
	try:
		Admin.objects.filter(adminID=username).get()
		admin = Admin.objects.get(adminID=username)
		if (password == admin.adminPW) & (admin.status==1):
			status = 2
		elif (password == admin.adminPW) & (admin.status==0):
			status = 1
			admin = Admin.objects.get(adminID=username)
			admin.status = 1
			admin.save()
	except:
		status=0
	return status

def index(request):
	user = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			admin = Admin.objects.get(adminID=username)
			print(admin.adminPW)
			user=admin.validate(password)
			print(user)
		except:
			return HttpResponse("Unknown User")
		if user==1:
			return redirect('floorplan', active=admin.status, user=username)
		elif user==0:
			return HttpResponse("Invalid login details given")
		else:
			admin.logout()
			return HttpResponse("Multiple Logins Detected! Logging Out All Instances!")
	else:
		return render(request, 'admin/login.html')

def floorplan(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/floorplan.html', context)
	else:
		return redirect('adminIndex')

def floorplan2(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/floorplan2.html', context)
	else:
		return redirect('adminIndex')

def approveConfirmation(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/approve.html', context)
	else:
		return redirect('adminIndex')

def editAllocation(request, active, user):
	admin = Admin.objects.get(adminID=user)
	#TODO: call API to get current allocation from db, to get teams that are in level 1
	allocation = {
    'clus1': {
        'clusPos':{'x':500.0, 'y':400.0},
        'clusAngle': 0.0,
		'clusLength': 200.0,
		'clusBreadth': 200.0,
        'teams':{
            'team1': {
		  'level':1, 
                  'industry':'industry1', 
                  'projectName':'project name 1', 
                  'sLength':100.0, 
                  'sWidth':100.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  },
            'team2': {
		  'level':1, 
                  'industry':'industry2', 
                  'projectName':'project name 2', 
                  'sLength':100.0, 
                  'sWidth':100.0, 
                  'relativeX':0.0, 
                  'relativeY':100.0
                  }
            }
        },
    'clus2': {
        
        'clusPos':{'x':0.0, 'y':0.0},
        'clusAngle':0.0,
		'clusLength': 200.0,
		'clusBreadth': 200.0,
        'teams':{
            'team3': {
		  'level':2,
                  'industry':'industry3', 
                  'projectName':'project name 3', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  },
            'team4': {
		  'level':2,
                  'industry':'industry4', 
                  'projectName':'project name 4', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  }
            }
        }
    }

	#loop through, keeping only those with level 1
	lvl_1_allocation = {}
	for cluster in list(allocation.keys()):
		for team in list((allocation[cluster])["teams"].keys()):
			if((((allocation[cluster])["teams"])[team])["level"] == 1):
				if(cluster in list(lvl_1_allocation.keys())):
					continue
				else:
				    lvl_1_allocation[cluster] = allocation[cluster]

	allocation_data = json.dumps(lvl_1_allocation)
	context = {'adminID':user, 'active':active}
	context['allocation'] = allocation_data
	if (active==admin.status) & (active==1):
		return render(request, 'admin/edit.html', context)
	else:
		return redirect('adminIndex')

def editAllocation2(request, active, user):
	admin = Admin.objects.get(adminID=user)
	#TODO: call API to get current allocation from db, to get teams that are in level 1
	allocation = {
    'clus1': {
        'clusPos':{'x':0.0, 'y':0.0},
        'clusAngle': 0.0,
		'clusLength': 200.0,
		'clusBreadth': 200.0,
        'teams':{
            'team1': {
		  'level':1, 
                  'industry':'industry1', 
                  'projectName':'project name 1', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  },
            'team2': {
		  'level':1, 
                  'industry':'industry2', 
                  'projectName':'project name 2', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  }
            }
        },
    'clus2': {
        
        'clusPos':{'x':0.0, 'y':0.0},
        'clusAngle':0.0,
		'clusLength': 200.0,
		'clusBreadth': 200.0,
        'teams':{
            'team3': {
		  'level':2,
                  'industry':'industry3', 
                  'projectName':'project name 3', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  },
            'team4': {
		  'level':2,
                  'industry':'industry4', 
                  'projectName':'project name 4', 
                  'sLength':0.0, 
                  'sWidth':0.0, 
                  'relativeX':0.0, 
                  'relativeY':0.0
                  }
            }
        }
    }

	#loop through, keeping only those with level 2
	lvl_2_allocation = {}
	for cluster in list(allocation.keys()):
		for team in list((allocation[cluster])["teams"].keys()):
			if((((allocation[cluster])["teams"])[team])["level"] == 2):
				if(cluster in list(lvl_2_allocation.keys())):
					continue
				else:
				    lvl_2_allocation[cluster] = allocation[cluster]

	allocation_data = json.dumps(lvl_2_allocation)
	context = {'adminID':user, 'active':active}
	context['allocation'] = allocation_data
	if (active==admin.status) & (active==1):
		return render(request, 'admin/edit2.html', context)
	else:
		return redirect('adminIndex')

def viewRequirements(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		r=Request.objects.all()
		print("r in viewRequirements is:")
		print(r)
		context['request'] = r
		return render(request, 'admin/view.html', context)
	else:
		return redirect('adminIndex')

def logout(request, user):
	admin = Admin.objects.get(adminID=user)
	admin.status=0
	admin.save()
	return redirect('adminIndex')
