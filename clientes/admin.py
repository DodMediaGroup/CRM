from django.contrib import admin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from clientes.models import *
class AuthorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Departamento,AuthorAdmin)
admin.site.register(Municipio,AuthorAdmin)
admin.site.register(Cliente,AuthorAdmin)