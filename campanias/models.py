from django.db import models
from almacenes.models import Almacen
from datetime import datetime
# Create your models here.

class Campania(models.Model):
	identificador= models.AutoField(primary_key=True)
	nombre= models.CharField(max_length=100, null=False)
	estado= models.BooleanField()
	fecha_inicio= models.DateTimeField() #Cambiar por datetime
	fecha_fin= models.DateTimeField()
	descripcion= models.CharField(max_length=750, null=False)
	valor_boleta= models.IntegerField()

	def __unicode__(self):
		return unicode(self.nombre)

	class Meta:
		permissions = (("view_campania","Ver Campanias"),)

	def get_almacenes_participantes(self):
		result=[]
		almacenes= self.campaniaalmacen_set.all()[:5]
		for a in almacenes:
			result.append(a.almacen)
		if len(result)==5:
			result.append("Entre otros")
		return result

	def porcentaje_campania(self):
		porcentaje=0
		ahora= datetime.now()
		rango= (self.fecha_fin - self.fecha_inicio).days
		tiempo_transcurrido= (ahora - self.fecha_inicio).days
		resultado= float((100*tiempo_transcurrido)/rango)
		if resultado>100:
			return 100
		elif resultado<0 :
			return 0
		else:
			return resultado

class CampaniaAlmacen(models.Model):
	identificador= models.AutoField(primary_key=True)
	participa= models.BooleanField(default=True)
	almacen= models.ForeignKey(Almacen)
	campania= models.ForeignKey(Campania)