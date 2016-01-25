from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from clientes.models import *
from boletas.models import *
from campanias.models import *
from django.template import RequestContext
import json
from django.db import connection
from datetime import date

@login_required(login_url='/')
def index(request):
	# Clientes
	clientes= Cliente.objects.all()
	# Campanias
	cursor = connection.cursor()
	cursor.execute('SELECT MONTH(fecha) mes, SUM(valor_factura) valor FROM boletas_boleta WHERE YEAR(fecha)=YEAR(NOW()) GROUP BY MONTH(fecha)')
	resultado= cursor.fetchall()
	evolucionCampanias=[]
	for r in resultado:
		evolucionCampanias.append({'mes':str(r[0]).zfill(2),'valor':r[1]})
	# Numero de campanias regustradas en el anio actual
	numero_campanias= Campania.objects.filter(fecha_inicio__year=date.today().year)
	# Campanias activas con estadisticas
	cursor.execute('SELECT c.identificador, c.valor_boleta , COUNT(b.valor_factura) numero_boletas, SUM(b.valor_factura) valor, c.nombre campania FROM boletas_boleta b, campanias_campania c WHERE b.campania_id= c.identificador AND c.estado=1 GROUP BY c.nombre')
	resultado= cursor.fetchall()
	campanias_activas=[]
	for r in resultado:
		campanias_activas.append({'nombre':r[4],'recaudado':r[3],'numero_boletas':r[2],'valor_boleta':r[1],'id':r[0]})

	return render_to_response('crm/index.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def generarReporteClientes(request):
	estadistica= json.loads(request.GET['diccionario'])
	return render_to_response('crm/reporte_genero_edad.html',locals(), context_instance=RequestContext(request))