# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from shorter.models import Url, FetchLog

import random
import string
import re
import json

url_length = 4

allowed_schemes = ['http', 'https', 'ftp']
URL_REGEX = "(http|https|ftp):\/\/(.*)"

def genurl():
	return "".join(random.sample(string.ascii_lowercase+string.digits, url_length))

def index(request):
	if request.method == "GET":
		return render(request, "index.html")
	elif request.method == "POST":
		# test if post content has url
		try:
			longurl = request.POST["url"]
		except:
			return HttpResponse("format error")

		match = re.match(URL_REGEX, longurl)
		if not match:
			result = {	"status":"-1", 
						"longurl":longurl,
						"err_msg":"unsupported schemes"}
		else:
			try:
				url = Url.objects.get(longurl=longurl)
			except ObjectDoesNotExist:
				url = Url(longurl=longurl, tinyurl=genurl())
				url.save()
			tinyurl = url.tinyurl
			host = request.META["SERVER_NAME"]
			port = request.META["SERVER_PORT"]
			if port == "80":
				hostname = "http://"+host
			else:
				hostname = "http://%s:%s" % (host, port)
			tinyurl = hostname+"/"+url.tinyurl
			result = {	"status":"0",
						"longurl":longurl,
						"tinyurl":tinyurl}
		return HttpResponse(json.dumps(result))

def url(request, tinyurl=""):
	url = get_object_or_404(Url, tinyurl=tinyurl)
	ip = request.META["REMOTE_ADDR"]
	ua = request.META["HTTP_USER_AGENT"]
	try:
		refer = request.META["HTTP_REFERER"]
	except KeyError:
		refer = ""
	fetchlog = FetchLog(url=url, ip=ip, ua=ua, refer=refer)
	fetchlog.save()
	return HttpResponseRedirect(url.longurl)
