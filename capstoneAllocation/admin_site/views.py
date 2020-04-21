# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Admin, UploadedFiles, ReqData, AllocPic, Allocation
from .algorithm import run_Algorithm
from requirements.models import Team, Request
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime as dt
from itertools import chain
import pandas as pd
import csv
import json
import string
import random
from base64 import b64decode

################### Custom Functions #############################

def prepInput():
	data = ReqData.objects.filter(yearOfGrad=dt.now().year)
	if data.count != 0:
		projects = {}
		for i in data:
			r = ReqData.objects.get(teamID=i)
			specs={}
			specs['projectName'] = r.projectName
			specs['sLength'] = r.sLength
			specs['sWidth'] = r.sWidth
			specs['industry'] = r.industry
			projects[i.teamID] = specs
		return {'teams':projects}

def genPW():
	pw = ''
	for i in range(8):
		pw+=random.choice(list(string.ascii_letters+string.digits))
	if pw in Team.objects.values_list('teamPW', flat=True):
		pw=genPW()
	return pw

def resetEntries(year, numEntries):
	Request.objects.all().delete()
	Team.objects.all().delete()
	for i in range(1, numEntries+1):
		if i<10:
			t = str(year)+'00'+str(i)
		elif i<100:
			t = str(year)+'0'+str(i)
		else:
			t = str(year)+str(i)
		team = Team(pk=i, teamID=t, teamPW=genPW())
		team.save()
		req = Request(pk=i, teamID=t, yearOfGrad=year)
		req.save()

def separateLvl(allocation, lvl):
	lvl_allocation = {}

	if lvl == 1:
		#loop through, keeping only those with level 1]
		for team in list(allocation.keys()):
			if((allocation[team])["level"] == 1):
				lvl_allocation[team] = allocation[team]
	elif lvl == 2:
		#loop through, keeping only those with level 2
		for team in list(allocation.keys()):
			if((allocation[team])["level"] == 2):
				lvl_allocation[team] = allocation[team]
	return lvl_allocation

	


################### View Functions################################
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
	nowLvl=admin.currLvl
	print(admin.currLvl)
	try:
		img =  AllocPic.objects.filter(lvl=nowLvl).last().alloc
		context = {'adminID':user, 'active':active, 'floorplan': {'image':img, 'currLvl':admin.currLvl, 'nxtLvl': admin.nxtFpLvl('get')}}
	except:
		print("No image yet!")
		context = {'adminID':user, 'active':active, 'floorplan': {'currLvl':admin.currLvl, 'nxtLvl': admin.nxtFpLvl('get')}}
	
	if (active==admin.status) & (active==1):
		if request.method == 'POST':
			if 'runAlgo' in request.POST:
				data = prepInput()
				try:
					output = run_Algorithm(data)
					clusProj = output.return_projects()
					lvl1 = separateLvl(clusProj, 1)
					binData = json.dumps(lvl1).encode('utf-8')
					alloc1 = Allocation(allocation=binData, lvl=1)
					alloc1.save()
					lvl2 = separateLvl(clusProj, 2)
					binData2 = json.dumps(lvl2).encode('utf-8')
					alloc2 = Allocation(allocation=binData2, lvl=2)
					alloc2.save()
				except:
					return HttpResponse("Invalid response present")
			elif 'chgLvl' in request.POST:
				admin.nxtFpLvl('set')
				print(admin.currLvl)
				return redirect('floorplan', user=admin, active=active)
			else:
				try:
					request.FILES['myfile']
					myfile = request.FILES['myfile']
					f=UploadedFiles(yearOfGrad=request.POST["year"], fileName=myfile.name, uploadedFile=myfile)
					f.save()
					df=f.manageFile()
					output, dim = f.convertDfToDB(df, request.POST["year"])
					df=f.updateDimToData(output, dim)
					f.inputDB(df)
					return HttpResponse("File Uploaded")
				except MultiValueDictKeyError:
					return render('admin/floorplan.html', context)
		return render(request, 'admin/floorplan.html', context)
	else:
		return redirect('adminIndex')

def approveConfirmation(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (active==admin.status) & (active==1):
		r=Request.objects.all().order_by('pk')
		tPw=Team.objects.all().only('teamPW').order_by('pk')
		concat = []
		for i in range(r.count()):
			concat.append({"req":r[i], "tPw":tPw[i]})
		context['request'] = concat
		if request.method == 'POST':
			if (len(request.POST.get('yearOfEntry'))==4):
				try:
					year = int(request.POST.get('yearOfEntry'))
					numEntries = int(request.POST.get('numEntries'))
				except:
					return render(request, 'admin/approve.html', context)
				finally:
					resetEntries(year, numEntries)
			return redirect('approve', user=admin, active=active)
		return render(request, 'admin/approve.html', context)
	else:
		return redirect('adminIndex')

def approve(request, active, user):
	admin = Admin.objects.get(adminID=user)
	context = {'adminID':user, 'active':active}
	if (admin.isLoggedIn()) & (active==1):
		ReqData.objects.filter(yearOfGrad=dt.now().year).delete()
		r = Request.objects.all()
		for entry in r:
			entry.injectToDB()
		return render(request, 'admin/confirmation.html',context)
	else:
		return redirect('adminIndex')

def editAllocation(request, active, user):
	admin = Admin.objects.get(adminID=user)
	#TODO: call API to get current allocation from db, to get teams that are in level 1
	if request.method == 'POST':
		# print(request.POST['img'])
		img = request.POST['img']
		imgID = dt.now().strftime("%m%d%y-%H%M")
		AllocPic(savedDT=imgID, lvl=1, alloc=img).save()
	try:
		projects = Allocation.objects.filter(lvl=1).last()
		allocation = projects.unpackBinData()
		allocation_data = json.dumps(allocation)
	except:
		allocation_data = json.dumps({})
	context = {'adminID':user, 'active':active}
	context['allocation'] = allocation_data
	if (active==admin.status) & (active==1):
		return render(request, 'admin/edit.html', context)
	else:
		return redirect('adminIndex')

def editAllocation2(request, active, user):
	admin = Admin.objects.get(adminID=user)
	#TODO: call API to get current allocation from db, to get teams that are in level 1
	if request.method == 'POST':
		# print(request.POST['img'])
		img = request.POST['img']
		imgID = dt.now().strftime("%m%d%y-%H%M")
		AllocPic(savedDT=imgID, lvl=2, alloc=img).save()
	try:
		projects = Allocation.objects.filter(lvl=2).last()
		allocation = projects.unpackBinData()
		allocation_data = json.dumps(allocation)
	except:
		allocation_data = json.dumps({})
	context = {'adminID':user, 'active':active}
	context['allocation'] = allocation_data
	if (active==admin.status) & (active==1):
		return render(request, 'admin/edit2.html', context)
	else:
		return redirect('adminIndex')

def viewRequirements(request, active, user):
	admin = Admin.objects.get(adminID=user)
	years = ReqData.objects.values('yearOfGrad').distinct().order_by('-yearOfGrad')
	print(years)
	context = {'adminID':user, 'active':active, 'years':years}
	if (active==admin.status) & (active==1):
		if request.method == 'GET':
			yearOfGrad=request.GET.get('yearOfGrad')
			r=ReqData.objects.filter(yearOfGrad=yearOfGrad)
			context['request'] = r
			return render(request, 'admin/view.html', context)
		else:
			return render(request, 'admin/view.html', context)
	else:
		return redirect('adminIndex')

def logout(request, user):
	admin = Admin.objects.get(adminID=user)
	admin.logout()
	admin.currLvl=1
	admin.save()
	return redirect('adminIndex')

################### Space Allocation POST Request Functions################################

#When the Level 1 allocation is saved
def saveAllocation1(request, active, user):
	if(request.method == 'POST'):
		allocation_data = json.loads(request.body)
		binData = json.dumps(allocation_data).encode('utf-8')
		print(1)
		alloc = Allocation(allocation=binData, lvl=1)
		alloc.save()
		print(allocation_data)
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)

#When level 2 allocation is saved
def saveAllocation2(request, active, user):
	if(request.method == 'POST'):
		allocation_data = json.loads(request.body)
		binData = json.dumps(allocation_data).encode('utf-8')
		print(2)
		alloc = Allocation(allocation=binData, lvl=2)
		alloc.save()
		print(allocation_data)
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)
