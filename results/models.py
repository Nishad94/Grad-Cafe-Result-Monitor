from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class resultItem(models.Model):
	school = models.CharField(max_length=200)
	branch = models.CharField(max_length=200)
	degree = models.CharField(max_length=20)
	stats = models.CharField(max_length=1000)
	via = models.CharField(max_length=200)
	decision = models.CharField(max_length=200)
	time_added = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.school


# UCI$Computer Science$Masters
class gcUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	choice_schools_branch_degree = models.CharField(max_length = 1000)
	enable_email = models.BooleanField(default=True)
	def __str__(self):
		return self.user.username