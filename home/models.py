from django.db import models
from martor.models import MartorField

# Create your models here.
class TKB(models.Model):
	class_name = models.CharField(max_length=5, primary_key=True)
	TKB_content = models.TextField(max_length=1000, default=',,,,,\n,,,,,\n,,,,,\n,,,,,\n,,,,,')
	def __str__(self):
		return self.class_name

class NewFeed(models.Model):
	post_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	description = MartorField(max_length=10000)
	loi_hs = models.TextField(max_length=10000, default='', blank=True)
	publish_date = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta(object):
		ordering = ['-publish_date']

	def __str__(self):
		return self.title