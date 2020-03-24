from django.db import models

# Create your models here.

class Admin(models.Model):

	adminID = models.CharField(max_length=100)
	adminPW = models.CharField(max_length=100, default='password')
	status = models.IntegerField(default=0)
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