from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from campanias.models import Campania, CampaniaAlmacen
from almacenes.models import Almacen, Categoria
from django.db import connection
from django.template import RequestContext
import json
from datetime import date

@login_required(login_url='/')
@user_passes_test(lambda u: "campanias.view_campania" in u.get_all_permissions(), login_url='/')
def index(request):
	if request.method=='POST':
		campania= Campania()
		campania.nombre= request.POST['nombre']
		#fecha inicio
		var= request.POST['fecha_inicio'].split('/')
		campania.fecha_inicio= var[2]+"-"+var[0]+'-'+var[1]+' '
		#agregamos la hora tambien
		campania.fecha_inicio+= request.POST['hora_inicio']+':00'
		#fecha inicio
		var= request.POST['fecha_fin'].split('/')
		campania.fecha_fin= var[2]+"-"+var[0]+'-'+var[1]+' '
		campania.fecha_fin += request.POST['hora_fin']+':00'

		campania.estado=1
		campania.valor_boleta= request.POST['valor_boleta']
		campania.descripcion= request.POST['descripcion']

		try:
			#campania.save()
			#Ahora creamos el evento en la base de datos para que se cierre
			#al momento de la fecha 
			cursor = connection.cursor()
			cursor.execute("CREATE	EVENT "+campania.identificador+"_campania_event ON SCHEDULE AT '"+campania.fecha_fin+"' DO BEGIN UPDATE campanias_campania SET estado= 0 where id="+campania.identificador+"; END$$ DELIMITER;")
			#Agregar los almacenes a la campania
			almacenes= Almacen.objects.all()
			for a in almacenes:
				campania_almacen=CampaniaAlmacen()
				campania_almacen.participa=1
				campania_almacen.almacen=a
				campania_almacen.campania=campania
				#campania_almacen.save()
			campanias= Campania.objects.all()
			
			return render(request,'campanias/index.html',{'campanias':campanias,'mensaje_exito':campania.nombre.upper()+' Agregada exitosamente. APLICA PARA TODOS LOS ALMACENES POR DEFAULT'})
		except Exception, e:
			raise e
			campanias= Campania.objects.all()
			
			return render(request,'campanias/index.html',{'campanias':campanias,'mensaje_error':'No se logro completar la operacion'})
	else:
		if 'id_eliminar' in request.GET:
			campania_eliminar= Campania.objects.get(pk=request.GET['id_eliminar'])
			campania_eliminar.delete();
			return HttpResponseRedirect("/campanias/")
		campanias= Campania.objects.all()
		# Campanias activas con estadisticas
		cursor = connection.cursor()
		cursor.execute('SELECT c.identificador, c.valor_boleta , COUNT(b.valor_factura) numero_boletas, SUM(b.valor_factura) valor, c.nombre campania FROM boletas_boleta b, campanias_campania c WHERE b.campania_id= c.identificador AND c.estado=1 GROUP BY c.nombre')
		resultado= cursor.fetchall()
		campanias_activas=[]
		for r in resultado:
			campanias_activas.append({'nombre':r[4],'recaudado':r[3],'numero_boletas':r[2],'valor_boleta':r[1],'id':r[0]})
		return render_to_response('campanias/index.html',locals(), context_instance=RequestContext(request))

@login_required(login_url="/")
@user_passes_test(lambda u: "campanias.change_campania" in u.get_all_permissions(), login_url='/')
def desactivarCampania(request):
	campania= Campania.objects.get(pk=request.GET['id_campania'])
	campania.estado= not campania.estado
	campania.save()
	return HttpResponseRedirect("/campanias/")

@login_required(login_url='/')
@user_passes_test(lambda u: "campanias.add_campania" in u.get_all_permissions(), login_url='/')
def agregarCampania(request):
	if request.method=='POST':
		campania= Campania()
		campania.nombre= request.POST['nombre']
		#fecha inicio
		var= request.POST['fecha_inicio'].split('/')
		campania.fecha_inicio= var[2]+"-"+var[0]+'-'+var[1]+' '
		#agregamos la hora tambien
		campania.fecha_inicio+= request.POST['hora_inicio']+':00'
		#fecha inicio
		var= request.POST['fecha_fin'].split('/')
		campania.fecha_fin= var[2]+"-"+var[0]+'-'+var[1]+' '
		campania.fecha_fin += request.POST['hora_fin']+':00'

		campania.estado=1
		campania.valor_boleta= request.POST['valor_boleta']
		campania.descripcion= request.POST['descripcion']
		try:
			campania.save()
			#Agregar los almacenes a la campania
			almacenes= Almacen.objects.all()
			for a in almacenes:
				campania_almacen=CampaniaAlmacen()
				campania_almacen.participa=1
				campania_almacen.almacen=a
				campania_almacen.campania=campania
				campania_almacen.save()
			almacenes= CampaniaAlmacen.objects.filter(campania_id=campania.identificador)
			categorias= Categoria.objects.all()
			
			return HttpResponseRedirect("/campanias/editar-almacenes-campania/?id="+str(campania.pk))
		except Exception, e:
			campanias= Campania.objects.all()
			return render(request,'campanias/agregar.html',{'campanias':campanias,'mensaje_error':'No se logro completar la operacion'})
	else:
		campanias= Campania.objects.all()
		return render(request,'campanias/agregar.html',{'campanias':campanias})

@login_required(login_url="/")
@user_passes_test(lambda u: "campanias.change_campania" in u.get_all_permissions(), login_url='/')
def editarAlmacenesCampania(request):
	id_campania=request.GET['id']
	campania= Campania.objects.get(pk=id_campania)
	almacenes_temp= Almacen.objects.filter(estado=True)
	almacenes=[]
	estado=''
	for a in almacenes_temp:
		if CampaniaAlmacen.objects.filter(campania=campania,almacen=a):
			estado='checked'
		almacenes.append({'almacen':a,'estado':estado})
		estado=''
	categorias= Categoria.objects.all()	
	return render(request,'campanias/editar.html',{'categorias':categorias,'almacenes':almacenes,'campania':campania})


@login_required(login_url="/")
@user_passes_test(lambda u: "campanias.change_campania" in u.get_all_permissions(), login_url='/')
def editarParticipacion(request):
	almacenes= json.loads(request.GET['almacenes'])
	campania= Campania.objects.get(pk=request.GET['id_campania'])

	relacionCampania= campania.campaniaalmacen_set.all()
	for r in relacionCampania:
		r.delete()

	for a in almacenes:
		almacen= Almacen.objects.get(pk=a)
		nuevaRelacion= CampaniaAlmacen(almacen=almacen,campania=campania)
		nuevaRelacion.save()

	return HttpResponse('Success')

@login_required(login_url='/')
def verCampania(request):
	campania= Campania.objects.get(pk=request.GET['id'])
	return render_to_response('campanias/ver_campania.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
@user_passes_test(lambda u: "campanias.change_campania" in u.get_all_permissions(), login_url='/')
def editarCampania(request):
	campania= Campania.objects.get(pk=request.GET['id'])
	if request.method=="POST":
		campania.nombre= request.POST['nombre']
		campania.descripcion= request.POST['descripcion']
		#fecha inicio
		var= request.POST['fecha_inicio'].split('/')
		campania.fecha_inicio= var[2]+"-"+var[0]+'-'+var[1]+' '
		#agregamos la hora tambien
		campania.fecha_inicio+= request.POST['hora_inicio']+':00'
		#fecha fin
		var= request.POST['fecha_fin'].split('/')
		campania.fecha_fin= var[2]+"-"+var[0]+'-'+var[1]+' '
		campania.fecha_fin += request.POST['hora_fin']+':00'
		campania.valor_boleta= request.POST['valor_boleta']
		
		campania.save()
		return HttpResponseRedirect("/campanias/editar-campania/?id="+str(campania.pk))
	return render_to_response('campanias/editar_campania.html',locals(), context_instance=RequestContext(request))

