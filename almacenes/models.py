from django.db import models

# Create your models here.

class Categoria(models.Model):
	identificador= models.AutoField(primary_key=True)
	nombre= models.CharField(max_length=100, null=False)
	estado= models.BooleanField(default=True)

	def __unicode__(self):
		return unicode(self.nombre)

	class Meta:
		permissions = (("view_categoria","Ver Categorias"),)

class Almacen(models.Model):
	tipo_documento= models.CharField(max_length=10, null=False)
	documento= models.CharField(max_length=20,null=False)
	identificador= models.AutoField(primary_key=True)
	nombre= models.CharField(max_length=100, null=False)
	numero_local= models.CharField(max_length=50,null=False)
	estado= models.BooleanField()
	categoria= models.ForeignKey(Categoria)
	nombre_admin= models.CharField(max_length=100, null=False)
	telefono=  models.CharField(max_length=100, null=False)
	pagina_web=  models.CharField(max_length=500, null=True)
	correo= models.CharField(max_length=500, null=False)
	facebook= models.CharField(max_length=500, null=True)
	twitter= models.CharField(max_length=500, null=True)

	def __unicode__(self):
		return unicode(self.nombre)

	class Meta:
		permissions = (("view_almacen","Ver Almacenes"),)