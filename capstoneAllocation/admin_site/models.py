from django.db import models
from datetime import datetime as dt
import pandas as pd
import math
import json

# Create your models here.

class Admin(models.Model):

	adminID = models.CharField(max_length=100)
	adminPW = models.CharField(max_length=100, default='password')
	status = models.IntegerField(default=0)
	currLvl = models.IntegerField(default=1)
	isStaff = models.IntegerField(default=1)

	def __str__(self):
		return self.adminID

	def isLoggedIn(self):
		if self.status == 1:
			return True
		else:
			return False
	
	def validate(self, password):
		retStatus = 0
		# retStatus {0:Invalid, 1:Valid and Single Instance, 2:Multiple Instance}
		try:
			if (password == self.adminPW) & (self.status==1):
				retStatus=2
			elif (password == self.adminPW) & (self.status==0):
				retStatus = 1
				self.status=1
				self.save()
		except:
			retStatus=0
		return retStatus

	def logout(self):
		self.status=0
		self.save()

	def nxtFpLvl(self, mode):
		if mode=='set':
			self.currLvl = self.currLvl%2+1
			self.save()
		elif mode=='get':
			return self.currLvl%2+1

	def getFp(self, lvl):
		if lvl == 1:
			return 'images/lvl1floorplan.png'
		elif lvl == 2:
			return 'images/lvl2floorplan.png'
	

class UploadedFiles(models.Model):
	yearOfGrad = models.IntegerField(default=dt.now().year)
	fileName=models.CharField(max_length=100)
	uploadedFile=models.FileField(upload_to='documents/')

	def __str__(self):
		return self.yearOfGrad

	def manageFile(self):
		if '.csv' in self.fileName:
			df=pd.DataFrame(pd.read_csv(self.uploadedFile))
		elif '.xlsx' in self.fileName:
			df=pd.DataFrame(pd.read_excel(self.uploadedFile))
		return df

	def updateDimToData(self, df, dim):
		for i in dim:
			length=[]
			width=[]
			height=[]
			for j in dim[i]:
				print(j)
				dimensionsDict={'Length':0.0, 'Width':0.0, 'Height':0.0}
				if type(j)==str:
					stringls=j.split('x')
					newls=[]
					for k in stringls:
						if 'm' in k:
							newls.append(k.split('m')[0])
						else:
							newls.append(k.split(' ')[0])

					try:
						dimensionsDict['Length']=float(newls[0])
						dimensionsDict['Width']=float(newls[1])
						dimensionsDict['Height']=float(newls[2])
					except:
						pass
				length.append(dimensionsDict['Length'])
				width.append(dimensionsDict['Width'])
				height.append(dimensionsDict['Height'])
			toUpdate={(i+'Length'):length,(i+'Width'):width,(i+'Height'):height}
			df.update(toUpdate)
		return df

	def convertDfToDB(self, df, year):
		teamIDls = []
		yearOfGradls = []
		projectNamels = []
		pTypels = []
		repEmaills = []
		pDimls = []
		sDimls = []
		numPPls = []
		numBigPedls = []
		numSmallPedls = []
		pedDescls = []
		numMonitorls = []
		numTVls = []
		numTablels = []
		numChairls = []
		numHDMIls = []
		otherls = []

		for ind, entry in df.iterrows():
			if not math.isnan(entry['Exhibit']):
				teamIDls.append(entry['Exhibit'])
				yearOfGradls.append(year)
				projectNamels.append(entry['Unnamed: 1'])
				pTypels.append(entry['Unnamed: 3'])
				repEmaills.append('')
				numPPls.append(entry['No. of Power Points Needed:'])
				numBigPedls.append(entry['Pedestal(s):'])
				numSmallPedls.append(entry['Unnamed: 8'])
				pedDescls.append(entry['Unnamed: 9'])
				numMonitorls.append(entry['Other Requests:'])
				numTVls.append(entry['Unnamed: 11'])
				numTablels.append(entry['Unnamed: 12'])
				numChairls.append(entry['Unnamed: 13'])
				numHDMIls.append(entry['Unnamed: 15'])
				otherls.append(entry['Unnamed: 17'])
				pDimls.append(entry['Size and Weight of Physical Prototype:'])
				sDimls.append(entry['Showcase Space Needed: L x W x H'])

		output = {
				'teamID':teamIDls,
				'yearOfGrad':yearOfGradls,
				'projectName':projectNamels,
				'pType':pTypels,
				'repEmail':repEmaills,
				'pLength':[],
				'pWidth':[],
				'pHeight':[],
				'sLength':[],
				'sWidth':[],
				'sHeight':[],
				'numPP':numPPls,
				'numBigPed':numBigPedls,
				'numSmallPed':numSmallPedls,
				'pedDesc':pedDescls,
				'numMonitor':numMonitorls,
				'numTV':numTVls,
				'numTable':numTablels,
				'numChair':numChairls,
				'numHDMI':numHDMIls,
				'other':otherls,
				}

		dim = {'p':pDimls, 's':sDimls}

		return output, dim

	def inputDB(self, df):
		df=pd.DataFrame(df)
		for line in df.itertuples():
			checkData={
						'numPP':line.numPP,
						'numBigPed':line.numBigPed,
						'numSmallPed':line.numSmallPed,
						'numMonitor':line.numMonitor,
						'numTV':line.numTV,
						'numTable':line.numTable,
						'numChair':line.numChair,
						'numHDMI':line.numHDMI
						}
			for i in checkData:
				try:
					float(checkData[i])
				except:
					checkData[i] = 0.0
			r=ReqData(
				teamID=line.teamID,
				yearOfGrad=line.yearOfGrad,
				projectName = line.projectName,
				pType = line.pType,
				repEmail = line.repEmail,
				pLength = line.pLength,
				pWidth = line.pWidth,
				pHeight = line.pHeight,
				sLength = line.sLength,
				sWidth = line.sWidth,
				sHeight = line.sHeight,
				numPP = checkData['numPP'],
				numBigPed = checkData['numBigPed'],
				numSmallPed = checkData['numSmallPed'],
				pedDesc = line.pedDesc,
				numMonitor = checkData['numMonitor'],
				numTV = checkData['numTV'],
				numTable = checkData['numTable'],
				numChair = checkData['numChair'],
				numHDMI = checkData['numHDMI'],
				other = line.other
				)
			r.save()




class ReqData(models.Model):
	teamID = models.CharField(max_length=100)
	yearOfGrad = models.IntegerField(default=dt.now().year)
	projectName = models.CharField(max_length=100, null=True)
	pType = models.CharField(max_length=100, null=True)
	repEmail = models.EmailField(null=True)
	industry = models.CharField(max_length=100, null=True)
	pLength = models.FloatField(null=True)
	pWidth = models.FloatField(null=True)
	pHeight = models.FloatField(null=True)
	sLength = models.FloatField(null=True)
	sWidth = models.FloatField(null=True)
	sHeight = models.FloatField(null=True)
	numPP = models.FloatField(null=True)
	numBigPed = models.FloatField(null=True)
	numSmallPed = models.FloatField(null=True)
	pedDesc = models.CharField(max_length=500, null=True)
	numMonitor = models.FloatField(null=True)
	numTV = models.FloatField(null=True)
	numTable = models.FloatField(null=True)
	numChair = models.FloatField(null=True)
	numHDMI = models.FloatField(null=True)
	other = models.CharField(max_length=500, null=True)
	reqDateTime = models.DateTimeField(null=True)

	def __str__(self):
		return self.teamID

class Allocation(models.Model):
	allocateDT = models.DateTimeField(default=dt.now())
	allocation = models.BinaryField()
	lvl = models.FloatField()

	def __str__(self):
		return self.allocateDT

	def unpackBinData(self):
		return json.loads(self.allocation.decode('utf-8'))

	def inputDB(self):
		projects = json.loads(self.allocation.decode('utf-8'))
		teamID = ''
		projLvl = 0.0
		industry = ''
		projectName = ''
		sLength = 0.0
		sWidth = 0.0
		actualX = 0.0
		actualY = 0.0
		angle = 0.0

		for j in projects:
			teamID = j
			projLvl = projects[j]['level']
			industry = projects[j]['industry']
			projectName = projects[j]['projectName']
			sLength = projects[j]['sLength']
			sWidth = projects[j]['sWidth']
			actualX = projects[j]['actualX']
			actualY = projects[j]['actualY']
			angle = projects[j]['angle']
			entry = Project(
								teamID=teamID,
								projLvl=projLvl,
								industry = industry,
								projectName = projectName,
								sLength = sLength,
								sWidth = sWidth,
								actualX = actualX,
								actualY = actualY,
								angle = angle
								)
			entry.save()

class Project(models.Model):
	teamID = models.CharField(max_length=100)
	projLvl = models.FloatField(null=True)
	industry = models.CharField(max_length=100)
	projectName = models.CharField(max_length=100)
	sLength = models.FloatField(null=True)
	sWidth = models.FloatField(null=True)
	actualX = models.FloatField(null=True)
	actualY = models.FloatField(null=True)
	angle = models.FloatField(null=True)

	def __str__(self):
		return self.clusterID

class AllocPic(models.Model):

	savedDT = models.CharField(max_length=100)
	lvl = models.FloatField(null=True)
	alloc = models.TextField(null=True)

	def __str__(self):
		return self.savedDT
		