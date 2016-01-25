from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from almacenes.models import Almacen, Categoria
from campanias.models import Campania, CampaniaAlmacen
from boletas.models import *
import json
from django.http import Http404
from datetime import date
import datetime
from django.core import serializers
from django.template import RequestContext

@login_required(login_url='/')
@user_passes_test(lambda u: "almacenes.view_almacen" in u.get_all_permissions(), login_url='/')
def index(request):
	almacenes= Almacen.objects.filter(estado=True)
	return render(request,'almacenes/index.html',{'almacenes':almacenes})

@login_required(login_url="/")
@user_passes_test(lambda u: "almacenes.delete_almacen" in u.get_all_permissions(), login_url='/')
def desactivarAlmacen(request):
	almacen= Almacen.objects.get(pk=request.GET['id_eliminar'])
	boletas_relacionadas= almacen.boleta_set.all()
	if len(boletas_relacionadas)>0:
		almacen.estado=False
		almacen.save()
	else:
		almacen.delete()
	return HttpResponseRedirect("/almacenes/")

@login_required(login_url="/")
@user_passes_test(lambda u: "almacenes.add_almacen" in u.get_all_permissions(), login_url='/')
def agregarAlmacen(request):
	if request.method=='POST':
		try:
			almacen =Almacen()
			almacen.tipo_documento= request.POST['tipo_doc']
			almacen.documento= request.POST['documento']
			almacen.nombre= request.POST['nombres']
			almacen.numero_local= request.POST['local']
			almacen.estado=1
			#Categoria
			categoria= Categoria()
			categoria.identificador= request.POST['categoria']
			almacen.categoria= categoria
			#Fin
			almacen.nombre_admin= request.POST['apellidos']
			almacen.telefono= request.POST['telefono']
			almacen.pagina_web= request.POST['pagina_web']
			almacen.correo= request.POST['correo']
			almacen.facebook= request.POST['facebook']
			almacen.twitter= request.POST['twitter']
			almacen.save()

			categorias= Categoria.objects.filter(estado=True)
			
			return render(request,'almacenes/agregar.html',{'mensaje_exito':'El almacen '+almacen.nombre+' fue agregado correctamente','categorias':categorias})
		except Exception, e:
			raise e
			categorias= Categoria.objects.filter(estado=True)
			
			return render(request,'almacenes/agregar.html',{'mensaje_error':'No se logro completar la operacion','categorias':categorias})
		
	else:
		categorias= Categoria.objects.filter(estado=True)
		
		return render(request,'almacenes/agregar.html',{'categorias':categorias})

@login_required(login_url="/")
@user_passes_test(lambda u: "almacenes.add_almacen" in u.get_all_permissions(), login_url='/')
def agregarCategoria(request):
	if request.is_ajax:
		nombre= request.GET['nombre'].capitalize()
		try:
			busqueda= Categoria.objects.get(nombre=nombre,estado=True)
			return HttpResponse("Ya se encuentra registrada")
		except Exception, e:
			categoria= Categoria()
			categoria.nombre=nombre
			categoria.estado=1
			try:
				categoria.save()
				nuevas=Categoria.objects.filter(estado=True)
				data = serializers.serialize('json',nuevas)
				return HttpResponse(data, mimetype='application/json')
			except Exception, e:
				return HttpResponse("No se logro almacenar la categoria")
		return HttpResponse("Peticion valida")
	else:
		return HttpResponse("Peticion Invalida")

@login_required(login_url="/")
@user_passes_test(lambda u: "almacenes.view_almacen" in u.get_all_permissions(), login_url='/')
def verAlmacen(request):
	try:
		almacen=Almacen.objects.get(pk=request.GET['id_almacen'])
		campania_almacen=CampaniaAlmacen.objects.filter(participa=1,almacen_id=request.GET['id_almacen'])
		
		return render(request,'almacenes/ver.html',{'almacen':almacen,'campania_almacen':campania_almacen})
	except Exception, e:
		raise Http404("El contenido solicitado no existe")

@login_required(login_url="/")
@user_passes_test(lambda u: "almacenes.change_almacen" in u.get_all_permissions(), login_url='/')
def editarAlmacen(request):
	if request.method=='POST':
		try:
			almacen =Almacen()
			almacen.identificador= request.POST['identificador']
			almacen.tipo_documento= request.POST['tipo_doc']
			almacen.documento= request.POST['documento']
			almacen.nombre= request.POST['nombres']
			almacen.numero_local= request.POST['local']
			almacen.estado=1
			#Categoria
			categoria= Categoria()
			categoria.identificador= request.POST['categoria']
			almacen.categoria= categoria
			#Fin
			almacen.nombre_admin= request.POST['apellidos']
			almacen.telefono= request.POST['telefono']
			almacen.pagina_web= request.POST['pagina_web']
			almacen.correo= request.POST['correo']
			almacen.facebook= request.POST['facebook']
			almacen.twitter= request.POST['twitter']
			almacen.save()

			almacenes= Almacen.objects.all()
			
			return render(request,'almacenes/index.html',{'almacenes':almacenes,'mensaje_exito':'El almacen '+almacen.nombre+' se Modifico correctamente'})
		except Exception, e:
			raise e
			almacenes= Almacen.objects.all()
			categorias= Categoria.objects.filter(estado=True)
			
			return render(request,'almacenes/index.html',{'almacenes':almacenes,'mensaje_error':'No se logro completar la operacion','categorias':categorias})
		
	else:
		try:
			almacen=Almacen.objects.get(pk=request.GET['id_almacen'])
			categorias= Categoria.objects.filter(estado=True)
			
			return render(request,'almacenes/editar.html',{'almacen':almacen,'categorias':categorias})
		except Exception, e:
			raise Http404("El contenido solicitado no existe")
		

@login_required(login_url='/')
@user_passes_test(lambda u: "almacenes.view_categoria" in u.get_all_permissions(), login_url='/')
def categorias(request):
	if request.method=="POST":
		if request.POST['tipo']=="agregar":
			nueva_categoria= Categoria(nombre=request.POST['nombre'])
			busqueda= Categoria.objects.filter(nombre=request.POST['nombre'],estado=True)
			if len(busqueda)>0:
				mensaje_error="Ya se encuentra registrada una categoria de nombre similar a "+request.POST['nombre']
			else:
				nueva_categoria.save()
				mensaje_exito="Categoria almacenada"
	if "id" in request.GET:
		categoria= Categoria.objects.get(pk=request.GET['id'])
		almacenes_relacionados= categoria.almacen_set.all()
		if len(almacenes_relacionados)>0:
			# Si no tiene nada relacionado la categoria se elimina del todo
			categoria.estado=False
			categoria.save()
		else:	
			categoria.delete()
		mensaje_exito="Categoria borrada"
	categorias= Categoria.objects.filter(estado=True)
	return render_to_response('almacenes/categorias.html',locals(), context_instance=RequestContext(request))