from django.contrib import admin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from campanias.models import *
class AuthorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Campania,AuthorAdmin)
admin.site.register(CampaniaAlmacen,AuthorAdmin)