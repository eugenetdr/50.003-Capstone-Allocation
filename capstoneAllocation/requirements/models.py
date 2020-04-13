from django.db import models
from django.db import connection, transaction
import datetime
from admin_site.models import ReqData
from datetime import datetime as dt
import random as rand

class Team(models.Model):

	teamID = models.CharField(max_length=100)
	teamPW = models.CharField(max_length=100, default='password')
	yearOfGrad = models.IntegerField(default=dt.now().year)
	status = models.IntegerField(default=0)
	requestMade = models.IntegerField(default=0)
	isStaff = models.IntegerField(default=0)

	def __str__(self):
		return self.teamID
	
	def isLoggedIn(self):
		if self.status == 1:
			return True
		else:
			return False
	
	def validate(self, password):
		retStatus = 0
		# retStatus {0:Invalid, 1:Valid and Single Instance, 2:Multiple Instance}
		try:
			if (password == self.teamPW) & (self.status==1):
				retStatus=2
			elif (password == self.teamPW) & (self.status==0):
				retStatus = 1
				self.status=1
				self.save()
		except:
			retStatus=0
		return retStatus

	def logout(self):
		self.status=0
		self.save()

	def madeRequest(self):
		self.requestMade=1
		self.save()

	def populate(self, numEntries):
		for i in range(1, numEntries+1):
			req=Request.objects.get(pk=i)
			if i<10:
				tid = '202000'+str(i)
			elif i<100:
				tid = '2020'+str(i)
			else:
				tid = '2020'+str(i)
			sLength=rand.choice([1,1.5,2,1,1.5,2,3])
			sWidth=rand.choice([1,1.5,2,1,1.5,2,3])
			sHeight=rand.choice([1,1.5,2,1,1.5,2,3])
			pLength=sLength-0.2
			pWidth=sWidth-0.2
			pHeight=sHeight-0.2
			projectName='Capstone'+tid
			industry=rand.choice(['Internet Security','Entrepreneurship','Mobile Application','Logistics','Robotics','Integrated Systems','Architecture','Defense'])
			repEmail=projectName+'@capstone.com'
			numPP = rand.choice([1,2,3])
			numBigPed = rand.choice([0,1])
			numSmallPed = rand.choice([0,1,2])
			pedDesc = rand.choice([
									'TESTTESTTESTTESTTEST',
									'TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST',
									'TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST'
									])
			numMonitor = rand.choice([0,1])
			numTV = rand.choice([0,1])
			numTable = rand.choice([0,1])
			numChair = rand.choice([0,1,2])
			numHDMI = numTV+numMonitor
			other = rand.choice([
									'TESTTESTTESTTESTTEST',
									'TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST',
									'TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST'
									])
			reqDateTime = dt.now()

			if (sLength==3 or sWidth==3 or sHeight==3):
				pType='1:1'
			else:
				pType=rand.choice(['1:1', 'Scaled Prototype', 'Software Prototype', 'Partial Prototype'])
			if industry == 'Internet Security' or industry == 'Mobile Application':
				pType = 'Software Prototype'
				sLength=1
				sWidth=1
				sHeight=1
				pLength=0.8
				pWidth=0.8
				pHeight=0.8
			if numBigPed+numSmallPed==0:
				pedDesc=''

			req.teamID=tid
			req.projectName=projectName
			req.repEmail=repEmail
			req.industry=industry
			req.pType=pType
			req.pLength=pLength
			req.pWidth=pWidth
			req.pHeight=pHeight
			req.sLength=sLength
			req.sWidth=sWidth
			req.sHeight=sHeight
			req.numPP=numPP
			req.numHDMI=numHDMI
			req.numBigPed=numBigPed
			req.numSmallPed=numSmallPed
			req.pedDesc=pedDesc
			req.numMonitor=numMonitor
			req.numTV=numTV
			req.numTable=numTable
			req.numChair=numChair
			req.other=other

			print(projectName, type(projectName))
			req.save()


class Request(models.Model):
	teamID = models.CharField(max_length=100)
	yearOfGrad = models.IntegerField(default=dt.now().year)
	projectName = models.CharField(max_length=100, null=True)
	pType = models.CharField(max_length=100, null=True)
	industry = models.CharField(max_length=100, null=True)
	repEmail = models.EmailField(null=True)
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

	def inputDetails(self, detailsDict):
		self.projectName = detailsDict['projectName']
		self.pType = detailsDict['prototypeType']
		self.industry = detailsDict['industry']
		self.repEmail = detailsDict['representativeEmail']
		self.pLength = detailsDict['prototypeLength']
		self.pWidth = detailsDict['prototypeWidth']
		self.pHeight = detailsDict['prototypeHeight']
		self.sLength = detailsDict['showcaseLength']
		self.sWidth = detailsDict['showcaseWidth']
		self.sHeight = detailsDict['showcaseHeight']
		self.numPP = detailsDict['powerpoints']
		self.numBigPed = detailsDict['bigPedestals']
		self.numSmallPed = detailsDict['smallPedestals']
		self.pedDesc = detailsDict['pedestalDescription']
		self.numMonitor = detailsDict['monitors']
		self.numTV = detailsDict['TVs']
		self.numTable = detailsDict['tables']
		self.numChair = detailsDict['chairs']
		self.numHDMI = detailsDict['HDMIAdaptors']
		self.other = detailsDict['others']
		self.reqDateTime = detailsDict['reqDateTime']
		self.save()

	def injectToDB(self):
		inject = ReqData(
							teamID = self.teamID,
							projectName = self.projectName,
							pType = self.pType,
							yearOfGrad = self.yearOfGrad,
							industry = self.industry,
							repEmail = self.repEmail,
							pLength = self.pLength,
							pWidth = self.pWidth,
							pHeight = self.pHeight,
							sLength = self.sLength,
							sWidth = self.sWidth,
							sHeight = self.sHeight,
							numPP = self.numPP,
							numBigPed = self.numBigPed,
							numSmallPed = self.numSmallPed,
							pedDesc = self.pedDesc,
							numMonitor = self.numMonitor,
							numTV = self.numTV,
							numTable = self.numTable,
							numChair = self.numChair,
							numHDMI = self.numHDMI,
							other = self.other,
							reqDateTime = self.reqDateTime,)
		inject.save()