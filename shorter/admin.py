from django.contrib import admin
from shorter.models import Url, FetchLog
from django.conf.urls import patterns, url

class UrlAdmin(admin.ModelAdmin):
	fields = ("tinyurl", "longurl")
	list_display = ("tinyurl", "longurl", "add_date")
	list_filter = ("add_date",)

class FetchLogAdmin(admin.ModelAdmin):
	fields = ("url", "ip", "ua", "refer")
	list_display = ("url", "ip", "ua", "refer", "fetch_date")
	readonly_fields = ("url", "ip", "ua", "refer")
	list_filter = ("url", "ip", "fetch_date")

admin.site.register(Url, UrlAdmin)
admin.site.register(FetchLog, FetchLogAdmin)
