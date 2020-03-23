from django.db import models
# from django.contrib.auth.models import User

class Team(models.Model):

    teamID = models.CharField(max_length=100)
    teamPW = models.CharField(max_length=100, default='password')
    status = models.IntegerField(default=0)
    requestMade = models.IntegerField(default=0)
    isStaff = models.IntegerField(default=0)

    def __str__(self):
        return self.teamID

class Request(models.Model):
	teamID = models.CharField(max_length=100)
	projectName = models.CharField(max_length=100, null=True)
	pType = models.CharField(max_length=100, null=True)
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

	def __str__(self):
		return self.teamID


# class UserProfileInfo(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.user.username

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
    
#     def __str__(self):
#         return self.question_text

#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text
