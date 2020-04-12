from django.db import models
from django.db import connection, transaction
import datetime
from admin_site.models import ReqData
# from django.contrib.auth.models import User

class Team(models.Model):

	teamID = models.CharField(max_length=100)
	teamPW = models.CharField(max_length=100, default='password')
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


class Request(models.Model):
	teamID = models.CharField(max_length=100)
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