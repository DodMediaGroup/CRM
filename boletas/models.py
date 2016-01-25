from django.db import models
from campanias.models import Campania
from almacenes.models import Almacen
from clientes.models import Cliente

class Boleta(models.Model):
	identificador= models.AutoField(primary_key=True)
	campania= models.ForeignKey(Campania)
	almacen= models.ForeignKey(Almacen)
	cliente= models.ForeignKey(Cliente)
	fecha= models.DateTimeField()
	valor_factura= models.BigIntegerField()# En base a este valor se calcula el numero de boletas asignadas

	def __unicode__(self):
		return unicode(str(self.identificador)+" "+self.campania.nombre)

	class Meta:
		permissions = (("view_boleta","Ver Boletas"),)

