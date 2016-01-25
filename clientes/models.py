from django.db import models
from datetime import date

class Departamento(models.Model):
	identificador= models.AutoField(primary_key=True)
	nombre= models.CharField(max_length=100, null=False)

class Municipio(models.Model):
	identificador= models.AutoField(primary_key=True)
	departamento= models.ForeignKey(Departamento)
	nombre= models.CharField(max_length=100, null=False)

class Cliente(models.Model):
	documento= models.CharField(max_length=20,null=False,unique=True)
	tipo_documento= models.CharField(max_length=10, null=False)
	nombres= models.CharField(max_length=200, null=False)
	apellidos= models.CharField(max_length=200, null=False)
	genero= models.BooleanField()
	fecha_nacimiento= models.DateField()
	estado_civil= models.CharField(max_length=10, null=False)
	telefono= models.CharField(max_length=50, null=False)
	correo= models.CharField(max_length=250, null=False)
	direccion= models.CharField(max_length=500,null=False)
	ciudad= models.ForeignKey(Municipio)
	observaciones= models.CharField(max_length=250, default='Ninguna')

	def get_edad(self):
	    today = date.today()
	    try: 
	        birthday = self.fecha_nacimiento.replace(year=today.year)
	    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
	        birthday = self.fecha_nacimiento.replace(year=today.year, month=self.fecha_nacimiento.month+1, day=1)
	    if birthday > today:
	        return today.year - self.fecha_nacimiento.year - 1
	    else:
	        return today.year - self.fecha_nacimiento.year

	def __unicode__(self):
		return unicode(self.nombres+" "+self.apellidos)

	def get_fecha_nacimiento(self):
		fecha=""
		try:
			fecha= self.fecha_nacimiento.strftime("%m/%d/%Y")
		except Exception, e:
			pass
		return fecha

	class Meta:
		permissions = (("view_cliente","Ver Clientes"),)