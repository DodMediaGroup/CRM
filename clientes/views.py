from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from clientes.models import Cliente, Departamento, Municipio
from boletas.models import Boleta
import json
from datetime import date
from django.core import serializers
import csv
from django.db import connection
from cStringIO import StringIO
from django.http import Http404
import unicodedata
import os
from random import randint
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def normalizar_cadenas(vector):
	lista=[]
	for v in vector:
		try:
			lista.append(elimina_tildes(v))
		except Exception, e:
			print v
			lista.append(v)
	return lista

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def importarArchivoCsv(request):
	if request.method=='POST':
		delimitador=";"
		linea=1
		contenido= request.FILES['file'].read().split("\r\n")
		nuevos_clientes=[]
		mensaje_exito=""
		mensaje_error=""
		for c in contenido[1:]:
			linea=linea+1
			row= c.split(delimitador)
			if len(row[0])==0:
				break
			else:
				genero=True
				if row[4]=="0":
					genero=False
				try:
					cliente=Cliente(documento=row[0],tipo_documento=row[1],nombres=row[2],apellidos=row[3],genero=genero,fecha_nacimiento=date(randint(1930,2003),randint(1,12),randint(1,28)),estado_civil=row[6],telefono=row[7],correo=row[8],direccion=row[9],ciudad=Municipio.objects.get(nombre__icontains=row[10]),observaciones="")
					nuevos_clientes.append(cliente)
					mensaje_exito="Base de datos almacenada"
				except Exception, e:
					mensaje_error="Error al leer el archivo en la linea "+str(linea)+". Favor verifique sus datos y vuelva a intentarlo."
		# Una vez que se leyo el archivo y no genero problemas se inicia con el almacenamiento
		if mensaje_error:
			mensaje_exito=None
		else:
			for nc in nuevos_clientes:
				try:
					nc.save()
				except Exception, e:
					mensaje_warning="No se pudieron almacenar algunos registros. Es posible que ya se encuentren almacenados en la base de datos"
	clientes= Cliente.objects.all()
	return render_to_response('clientes/index.html',locals(), context_instance=RequestContext(request))

def calculate_age(born):
    today = date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

@login_required(login_url='/')
@user_passes_test(lambda u: "clientes.view_cliente" in u.get_all_permissions(), login_url='/')
def index(request):
	if 'id_eliminar' in request.GET:
		cliente= Cliente.objects.get(pk=request.GET['id_eliminar'])
		cliente.delete()
		return HttpResponseRedirect("/clientes/")
	clientes= Cliente.objects.all()
	return render(request,'clientes/index.html',{'clientes':clientes})

@login_required(login_url='/')
@user_passes_test(lambda u: "clientes.add_cliente" in u.get_all_permissions(), login_url='/')
def agregar(request):
	if request.method == 'POST':
		documento= request.POST['documento']
		tipo_doc= request.POST['tipo_doc']
		nombres= request.POST['nombres']
		apellidos= request.POST['apellidos']
		genero= int(request.POST['genero'])
		fecha_nacimiento= request.POST['fecha_nacimiento']
		estado_civil= request.POST['estado_civil']
		correo= request.POST['correo']
		direccion= request.POST['direccion']
		telefono= request.POST['telefono']
		ciudad= request.POST['ciudad']
		observaciones= request.POST['observaciones']
		var= fecha_nacimiento.split('/')
		fecha_nacimiento= var[2]+"-"+var[0]+'-'+var[1]
		departamentos= Departamento.objects.all()
		
		try:
			persona_reg= Cliente.objects.get(pk=documento)
			return render(request,'clientes/agregar.html',{'mensaje_error':'El documento '+documento+' ya se encuentra registrado','departamentos':departamentos})
		except Exception, e:
			try:
				cliente= Cliente(documento=documento,tipo_documento=tipo_doc,nombres=nombres,apellidos=apellidos,genero=genero,fecha_nacimiento=fecha_nacimiento,estado_civil=estado_civil,telefono=telefono,correo=correo,direccion=direccion,ciudad=Municipio.objects.get(pk=ciudad),observaciones=observaciones)
				cliente.save()
				return render(request,'clientes/agregar.html',{'mensaje_exito':'Se agrego el cliente exitosamente','departamentos':departamentos})
			except Exception, e:
				raise e
				return render(request,'clientes/agregar.html',{'mensaje_error':'No se logro completar la operacion','departamentos':departamentos})
	else:
		departamentos= Departamento.objects.all()
		
		return render(request,'clientes/agregar.html',{'departamentos':departamentos})

@login_required(login_url='/')
def buscarMunicipio(request):
	if request.is_ajax():
		id_departamento= request.GET['departamento_id']
		municipios= Municipio.objects.filter(departamento_id=id_departamento);
		data = serializers.serialize('json',municipios)
		return HttpResponse(data, mimetype='application/json')
	else:
		return HttpResponse("Peticion no valida")

@login_required(login_url="/")
@user_passes_test(lambda u: "clientes.change_cliente" in u.get_all_permissions(), login_url='/')
def editarCliente(request):
	#try:
	id_usuario=request.GET["id"]
	cliente= Cliente.objects.get(pk=id_usuario)
	if request.method=="POST":
		documento= request.POST['documento']
		tipo_doc= request.POST['tipo_doc']
		nombres= request.POST['nombres']
		apellidos= request.POST['apellidos']
		genero= int(request.POST['genero'])
		fecha_nacimiento= request.POST['fecha_nacimiento']
		estado_civil= request.POST['estado_civil']
		correo= request.POST['correo']
		direccion= request.POST['direccion']
		telefono= request.POST['telefono']
		ciudad= request.POST['ciudad']
		observaciones= request.POST['observaciones']

		var= fecha_nacimiento.split('/')
		fecha_nacimiento= var[2]+"-"+var[0]+'-'+var[1]
		validador=True
		if not cliente.documento==documento or not cliente.tipo_documento==tipo_doc:
			if len(Cliente.objects.filter(documento=documento,tipo_documento=tipo_doc))>0:
				validador=False
		
		if validador:
			cliente.documento=documento
			cliente.tipo_documento= tipo_doc
			cliente.nombres=nombres
			cliente.apellidos= apellidos
			cliente.genero= genero
			cliente.fecha_nacimiento= fecha_nacimiento
			cliente.estado_civil= estado_civil
			cliente.correo= correo
			cliente.direccion= direccion
			cliente.telefono= telefono
			cliente.ciudad= Municipio.objects.get(pk=ciudad)
			cliente.observaciones= observaciones
			cliente.save()
			mensaje_exito="La informacion ha sido actualizada"
		else:
			mensaje_error="El documento que se intenta cambiar ya se encuentra registrado"

	cliente= Cliente.objects.get(pk=id_usuario)
	departamentos= Departamento.objects.all()
	municipios= Municipio.objects.filter(departamento=cliente.ciudad.departamento)
	return render_to_response('clientes/editar.html',locals(), context_instance=RequestContext(request))
	#except Exception, e:
	#	raise Http404("El contenido solicitado no existe")

@login_required(login_url='/')
@user_passes_test(lambda u: "clientes.view_cliente" in u.get_all_permissions(), login_url='/')
def verCliente(request):
	try:
		cliente = Cliente.objects.get(pk=request.GET['id'])
		boletas= Boleta.objects.filter(cliente_id=cliente.pk).order_by('-fecha')
		
		edad= calculate_age(cliente.fecha_nacimiento)
		return render(request,'clientes/ver.html',{'boletas':boletas,'edad':edad,'cliente':cliente})
	except Exception, e:
		raise Http404("El contenido solicitado no existe")

@login_required(login_url="/")
@user_passes_test(lambda u: "clientes.change_cliente" in u.get_all_permissions(), login_url='/')
def editarDireccion(request):
	if request.is_ajax:
		try:
			id_cliente=request.GET["id"]
			cliente= Cliente.objects.get(pk=id_cliente)
			cliente.direccion= request.GET['valor']
			cliente.save()
			return HttpResponse('Operacion exitosa')
		except Exception, e:
			return HttpResponse('Ocurrio un error')
	else:
		return HttpResponse('Peticion no valida')


@login_required(login_url="/")
@user_passes_test(lambda u: "clientes.change_cliente" in u.get_all_permissions(), login_url='/')
def editarTelefono(request):
	if request.is_ajax:
		try:
			id_cliente=request.GET["id"]
			cliente= Cliente.objects.get(pk=id_cliente)
			cliente.telefono= request.GET['valor']
			cliente.save()
			return HttpResponse('Operacion exitosa')
		except Exception, e:
			return HttpResponse('Ocurrio un error')
	else:
		return HttpResponse('Peticion no valida')

def exportarCsv(request):
#	try:
	ciudad= request.GET['ciudad']
	genero= request.GET['genero']
	edad= request.GET['edad']
	estado_civil= request.GET['estado_civil']

	aux="0";
	if genero=='Masculino':
		aux="1"

	consulta= 'SELECT c.documento, c.tipo_documento, c.nombres, c.apellidos, c.genero, c.fecha_nacimiento,((DATE_FORMAT( CURDATE( ) , "%%Y-%%m-%%d" ) - DATE_FORMAT( c.fecha_nacimiento, "%%Y-%%m-%%d" ) )) edad, c.estado_civil, c.telefono, c.correo, c.direccion, m.nombre ciudad'
	consulta+=" FROM clientes_cliente c, clientes_municipio m WHERE"
	consulta+=" c.ciudad_id = m.identificador"
	if ciudad != "":
		consulta+=" AND m.nombre LIKE '"+ciudad+"'"
	if estado_civil != "":
		consulta+=" AND c.estado_civil LIKE '"+estado_civil+"'"
	if genero=="":
		consulta+=" AND c.genero >= 0 "
	else:
		consulta+=" AND c.genero ="+aux

	vector= edad.split("-")
	consulta+=" AND ((DATE_FORMAT( CURDATE( ) , '%%Y-%%m-%%d' ) - DATE_FORMAT( c.fecha_nacimiento, '%%Y-%%m-%%d' ) )) BETWEEN "+vector[0]+" AND "+vector[1]
	
	cursor = connection.cursor()
	cursor.execute(consulta)
	row = cursor.fetchall()

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

	w= csv.writer(response)
	cabecera= ["Documento","Tipo Documento","Nombre","Apellidos","Genero","Fecha de Nacimiento","Edad","Estado Civil","Telefono","Correo","Direccion","Ciudad"]
	w.writerow(cabecera)
	for r in row:
		w.writerow(normalizar_cadenas(r))

	return response

#	except Exception, e:
#		raise e
#		return HttpResponse("Error") 