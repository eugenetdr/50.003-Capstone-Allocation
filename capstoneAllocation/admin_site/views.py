# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admin

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
	user = False
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = validate(username, password)
		if user==1:
			admin = Admin.objects.get(adminID=username)
			admin.status=1
			admin.save()
			return redirect('floorplan', active=admin.status, user=username)
		elif user==0:
			return HttpResponse("Invalid login details given")
		else:
			return HttpResponse("Multiple Logins Detected!")
	else:
		return render(request, 'admin/login.html')

def floorplan(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/floorplan.html', context)
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
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/edit.html', context)
	else:
		return redirect('adminIndex')

def viewRequirements(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		return render(request, 'admin/view.html', context)
	else:
		return redirect('adminIndex')

def logout(request, user):
	admin = Admin.objects.get(adminID=user)
	admin.status=0
	admin.save()
	return redirect('adminIndex')
