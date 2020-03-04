from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return render(request, 'admin/login.html')

def floorplan(request):
	return render(request, 'admin/floorplan.html')

def approveConfirmation(request):
	return render(request, 'admin/approve.html')

def editAllocation(request):
	return render(request, 'admin/edit.html')

def viewRequirements(request):
	return render(request, 'admin/view.html')