from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse("Hello, world. You're at the admin login page.")

def floorplan(request):
	return HttpResponse("floorplan page")

def approveConfirmation(request):
	return HttpResponse("approved confirmation page")

def editAllocation(request):
	return HttpResponse("edit floorplan page")

def viewRequirements(request):
	return HttpResponse("view requests page")