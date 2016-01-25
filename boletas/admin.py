from django.contrib import admin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from boletas.models import *
class AuthorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Boleta,AuthorAdmin)