from django.contrib import admin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from almacenes.models import *
class AuthorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Categoria,AuthorAdmin)
admin.site.register(Almacen,AuthorAdmin)