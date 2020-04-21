# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Admin, UploadedFiles, ReqData, AllocPic
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
	# admin.getFp(admin.currLvl)
	
	if (active==admin.status) & (active==1):
		if request.method == 'POST':
			if 'runAlgo' in request.POST:
				data = prepInput()
				print(data)
				try:
					print("\n\n\n\n\n\n")
					print(1)
					output = run_Algorithm(data)
					print("\n\n\n\n\n\n")
					print(2)
					alloc = output.return_projects()
					print("\n\n\n\n\n\n")
					print(alloc)
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
		print(request.POST['img'])
		img = request.POST['img']
		imgID = dt.now().strftime("%m%d%y-%H%M")
		AllocPic(savedDT=imgID, lvl=1, alloc=img).save()
	"""
	allocation = {
            'team1': {
                  'level': 1,
                  'industry':'industry1', 
                  'projectName':'project name 1', 
                  'sLength':100.0, 
                  'sWidth':100.0, 
                  'actualX':400.0, 
                  'actualY':400.0,
                  'angle':45.0
                },
            'team2': {
                  'level': 1,
                  'industry': 'industry2', 
                  'projectName': 'project name 2', 
                  'sLength': 200.0, 
                  'sWidth': 200.0, 
                  'actualX': 200.0, 
                  'actualY': 200.0,
                  'angle':45.0
        	}
		}
	"""
	
	
	allocation = {
'2020025': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020025', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 355.0, 'actualY': 255.0, 'angle': 0}, 
'2020024': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020024', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 371.4, 'actualY': 255.0, 'angle': 0}, 
'2020012': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020012', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 420.6, 'actualY': 255.0, 'angle': 0}, 
'2020100': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020100', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 476.5, 'actualY': 231.5, 'angle': 0}, 
'2020005': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020005', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 476.5, 'actualY': 264.3, 'angle': 0}, 
'2020054': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020054', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 492.5, 'actualY': 103.5, 'angle': 0}, 
'2020069': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020069', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 453.4, 'actualY': 255.0, 'angle': 0}, 
'2020050': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020050', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 492.5, 'actualY': 128.1, 'angle': 0}, 
'2020032': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020032', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 585.0, 'actualY': 267.5, 'angle': 0}, 
'2020084': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020084', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 617.8, 'actualY': 267.5, 'angle': 0}, 
'2020096': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020096', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 453.4, 'actualY': 271.4, 'angle': 0}, 
'2020075': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020075', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 525.7, 'actualY': 231.5, 'angle': 0}, 
'2020066': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020066', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 541.7, 'actualY': 103.5, 'angle': 0}, 
'2020057': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020057', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 558.1, 'actualY': 103.5, 'angle': 0}, 
'2020051': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020051', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 574.5, 'actualY': 103.5, 'angle': 0}, 
'2020047': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020047', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 590.9, 'actualY': 103.5, 'angle': 0}, 
'2020033': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020033', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 585.0, 'actualY': 283.9, 'angle': 0}, 
'2020027': {'level': 1, 'industry': 'Mobile Application', 'projectName': 'Capstone2020027', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 617.8, 'actualY': 292.1, 'angle': 0}, 
'2020039': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020039', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 642.4, 'actualY': 267.5, 'angle': 0}, 
'2020015': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020015', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 667.0, 'actualY': 267.5, 'angle': 0}, 
'2020095': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020095', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 477.4088206070769, 'actualY': 577.9910537936214, 'angle': -40}, 
'2020046': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020046', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 554.7703502372292, 'actualY': 514.9891795754169, 'angle': -40}, 
'2020030': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020030', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 612.7693481694967, 'actualY': 495.30440505303375, 'angle': -40}, 
'2020094': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020094', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 742.0, 'actualY': 220.0, 'angle': 0}, 
'2020072': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020072', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 791.2, 'actualY': 220.0, 'angle': 0}, 
'2020063': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020063', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 840.4, 'actualY': 220.0, 'angle': 0}, 
'2020059': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020059', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 889.6, 'actualY': 220.0, 'angle': 0}, 
'2020031': {'level': 1, 'industry': 'Logistics', 'projectName': 'Capstone2020031', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 725.0, 'actualY': 355.0, 'angle': 0}, 
'2020060': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020060', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 355.0, 'actualY': 271.4, 'angle': 0}, 
'2020014': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020014', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 525.7, 'actualY': 247.9, 'angle': 0}, 
'2020020': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020020', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 642.4, 'actualY': 292.1, 'angle': 0}, 
'2020071': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020071', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 482.66095247482525, 'actualY': 582.6411895051766, 'angle': -40}, 
'2020038': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020038', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 563.7368683660081, 'actualY': 511.32963541202946, 'angle': -40}, 
'2020073': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020073', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 667.0, 'actualY': 292.1, 'angle': 0}, 
'2020043': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020043', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 624.579780669179, 'actualY': 485.28256673034184, 'angle': -40}, '2020018': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020018', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 651.4836073795357, 'actualY': 543.3626948195988, 'angle': -40}, '2020016': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020016', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 742.0, 'actualY': 252.8, 'angle': 0}, '2020011': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020011', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 791.2, 'actualY': 252.8, 'angle': 0}, '2020067': {'level': 1, 'industry': 'Defense', 'projectName': 'Capstone2020067', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 840.4, 'actualY': 252.8, 'angle': 0}, '2020019': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020019', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 641.8475410895957, 'actualY': 540.3201259794132, 'angle': -40}, '2020089': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020089', 'sLength': 32.8, 'sWidth': 24.599999999999998, 'actualX': 889.6, 'actualY': 252.8, 'angle': 0}, '2020040': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020040', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 725.0, 'actualY': 387.8, 'angle': 0}, '2020008': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020008', 'sLength': 32.8, 'sWidth': 24.599999999999998, 'actualX': 848.0, 'actualY': 371.4, 'angle': 0}, '2020081': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020081', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 880.8, 'actualY': 371.4, 'angle': 0}, '2020045': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020045', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 780.0, 'actualY': 511.5, 'angle': 0}, '2020023': {'level': 1, 'industry': 'Integrated Systems', 'projectName': 'Capstone2020023', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 812.8, 'actualY': 511.5, 'angle': 0}, '2020076': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020076', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 774.2, 'actualY': 355.0, 'angle': 0}, '2020064': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020064', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 798.8, 'actualY': 355.0, 'angle': 0}, '2020061': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020061', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 823.4, 'actualY': 355.0, 'angle': 0}, '2020058': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020058', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 848.0, 'actualY': 355.0, 'angle': 0}, '2020055': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020055', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 880.8, 'actualY': 355.0, 'angle': 0}, '2020036': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020036', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 913.6, 'actualY': 355.0, 'angle': 0}, '2020010': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020010', 'sLength': 24.599999999999998, 'sWidth': 24.599999999999998, 'actualX': 938.2, 'actualY': 355.0, 'angle': 0}, '2020044': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020044', 'sLength': 32.8, 'sWidth': 24.599999999999998, 'actualX': 780.0, 'actualY': 544.3, 'angle': 0}, '2020026': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020026', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 812.8, 'actualY': 536.1, 'angle': 0}, '2020070': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020070', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 922.5, 'actualY': 212.5, 'angle': 0}, '2020068': {'level': 1, 'industry': 'Architecture', 'projectName': 'Capstone2020068', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 971.7, 'actualY': 212.5, 'angle': 0}, '2020041': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020041', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 541.7, 'actualY': 119.9, 'angle': 0}, '2020082': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020082', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 774.2, 'actualY': 371.4, 'angle': 0}, '2020074': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020074', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 798.8, 'actualY': 371.4, 'angle': 0}, '2020021': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020021', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 823.4, 'actualY': 371.4, 'angle': 0}, '2020013': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020013', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 913.6, 'actualY': 379.6, 'angle': 0}, '2020097': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020097', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 862.0, 'actualY': 511.5, 'angle': 0}, '2020083': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020083', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 922.5, 'actualY': 237.1, 'angle': 0}, '2020049': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020049', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 971.7, 'actualY': 245.3, 'angle': 0}, '2020034': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020034', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 1037.3, 'actualY': 245.3, 'angle': 0}, '2020009': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020009', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 1146.4, 'actualY': 237.8, 'angle': 0}, '2020029': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020029', 'sLength': 32.8, 'sWidth': 24.599999999999998, 'actualX': 1065.158153629854, 'actualY': 449.74813687163044, 'angle': 315}, '2020098': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020098', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 1083.0899745552067, 'actualY': 435.77084831236647, 'angle': 315}, '2020086': {'level': 1, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020086', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 1135.0850792606816, 'actualY': 437.02029699079793, 'angle': 315}, '2020004': {'level': 2, 'industry': 'Entrepreneurship', 'projectName': 'Capstone2020004', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 736.2, 'actualY': 158.0, 'angle': 0}, '2020001': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020001', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 558.1, 'actualY': 119.9, 'angle': 0}, '2020093': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020093', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 574.5, 'actualY': 119.9, 'angle': 0}, '2020092': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020092', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 590.9, 'actualY': 119.9, 'angle': 0}, '2020091': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020091', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 691.6, 'actualY': 267.5, 'angle': 0}, '2020090': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020090', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 938.8, 'actualY': 220.0, 'angle': 0}, '2020080': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020080', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 938.2, 'actualY': 379.6, 'angle': 0}, '2020077': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020077', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 862.0, 'actualY': 527.9, 'angle': 0}, '2020056': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020056', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 894.8, 'actualY': 527.9, 'angle': 0}, '2020052': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020052', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 1020.9, 'actualY': 212.5, 'angle': 0}, '2020042': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020042', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 1130.0, 'actualY': 205.0, 'angle': 0}, '2020037': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020037', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 1195.6, 'actualY': 205.0, 'angle': 0}, '2020028': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020028', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 1195.6, 'actualY': 221.4, 'angle': 0}, '2020017': {'level': 1, 'industry': 'Internet Security', 'projectName': 'Capstone2020017', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 1067.5932054461623, 'actualY': 433.5676535194257, 'angle': 315}, '2020003': {'level': 2, 'industry': 'Internet Security', 'projectName': 'Capstone2020003', 'sLength': 16.4, 'sWidth': 16.4, 'actualX': 687.0, 'actualY': 158.0, 'angle': 0}, '2020048': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020048', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 1037.3, 'actualY': 212.5, 'angle': 0}, '2020099': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020099', 'sLength': 49.199999999999996, 'sWidth': 32.8, 'actualX': 1146.4, 'actualY': 205.0, 'angle': 0}, '2020006': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020006', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 1073.6675131418858, 'actualY': 428.95193283526, 'angle': 315}, 
'2020007': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020007', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 1098.7736983444338, 'actualY': 418.18167975741096, 'angle': 315}, '2020062': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020062', 'sLength': 49.199999999999996, 'sWidth': 24.599999999999998, 'actualX': 1149.7483396408677, 'actualY': 418.97496782929477, 'angle': 315}, '2020002': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020002', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 703.4, 'actualY': 158.0, 'angle': 0}, '2020053': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020053', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 769.0, 'actualY': 158.0, 'angle': 0}, '2020078': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020078', 'sLength': 32.8, 'sWidth': 32.8, 'actualX': 801.8, 'actualY': 158.0, 'angle': 0}, '2020035': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020035', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 834.6, 'actualY': 158.0, 'angle': 0}, '2020065': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020065', 'sLength': 49.199999999999996, 'sWidth': 16.4, 'actualX': 834.6, 'actualY': 174.4, 'angle': 0}, '2020085': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020085', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 736.2, 'actualY': 190.8, 'angle': 0}, '2020087': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020087', 'sLength': 32.8, 'sWidth': 16.4, 'actualX': 769.0, 'actualY': 190.8, 'angle': 0}, '2020022': {'level': 1, 'industry': 'Robotics', 'projectName': 'Capstone2020022', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 894.8, 'actualY': 511.5, 'angle': 0}, '2020079': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020079', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 801.8, 'actualY': 190.8, 'angle': 0}, '2020088': {'level': 2, 'industry': 'Robotics', 'projectName': 'Capstone2020088', 'sLength': 24.599999999999998, 'sWidth': 16.4, 'actualX': 883.8, 'actualY': 158.0, 'angle': 0}}

	

	#loop through, keeping only those with level 1
	lvl_1_allocation = {}

	for team in list(allocation.keys()):
		if((allocation[team])["level"] == 1):
			lvl_1_allocation[team] = allocation[team]

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
	if request.method == 'POST':
		print(request.POST['img'])
		img = request.POST['img']
		imgID = dt.now().strftime("%m%d%y-%H%M")
		AllocPic(savedDT=imgID, lvl=2, alloc=img).save()
	allocation = {
            'team1': {
                  'level': 2,
                  'industry':'industry1', 
                  'projectName':'project name 1', 
                  'sLength':100.0, 
                  'sWidth':100.0, 
                  'actualX':200.0, 
                  'actualY':200.0,
                  'angle':0.0
                }
		}

	"""
            'team2': {
                  'level': 2,
                  'industry': 'industry2', 
                  'projectName': 'project name 2', 
                  'sLength': 200.0, 
                  'sWidth': 200.0, 
                  'actualX': 200.0, 
                  'actualY': 200.0,
                  'angle':0.0
        	}
	"""

	#loop through, keeping only those with level 2
	lvl_2_allocation = {}

	for team in list(allocation.keys()):
		if((allocation[team])["level"] == 2):
			lvl_2_allocation[team] = allocation[team]

	allocation_data = json.dumps(lvl_2_allocation)
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
		print(json.loads(allocation_data))
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)

#When level 2 allocation is saved
def saveAllocation2(request, active, user):
	if(request.method == 'POST'):
		allocation_data = json.loads(request.body)
		print(json.loads(allocation_data))
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)
