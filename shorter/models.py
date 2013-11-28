from django.db import models

import random, string

class Url(models.Model):
	longurl = models.CharField(max_length=1024)
	tinyurl = models.CharField(max_length=16, unique=True)
	add_date = models.DateTimeField("date created", auto_now=True)

	def __unicode__(self):
		if(len(self.longurl) > 32):
			longurl = self.longurl[:64]+"..."
		else:
			longurl = self.longurl
		return "%s : %s" % (self.tinyurl, longurl)

class FetchLog(models.Model):
	url = models.ForeignKey("Url")
	ip = models.CharField(max_length=39)
	ua = models.CharField(max_length=1024)
	refer = models.CharField(max_length=1024)
	fetch_date = models.DateTimeField("fetch date", auto_now=True)
