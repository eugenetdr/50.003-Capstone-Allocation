from django.db import models

# Create your models here.

class Admin(models.Model):

    adminID = models.CharField(max_length=100)
    adminPW = models.CharField(max_length=100, default='password')
    status = models.IntegerField(default=0)
    isStaff = models.IntegerField(default=1)

    def __str__(self):
        return self.adminID