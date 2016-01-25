from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib.auth.models import User
from boletas.models import Boleta
from almacenes.models import Almacen, Categoria
from clientes.models import *
from campanias.models import *
import json
from django.db import connection
from django.core import serializers
import unicodedata
# Librerias necesarias para generar un pdf
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.template import RequestContext

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

# Permiso para verificar si el usuario puede ver los reportes
def puedeVisualizar(user):
	if user.is_superuser:
		return True
	else:
		# Modulo_id=4 pertenece a reportes
		try:
			permiso= Usuario_Modulo.objects.get(usuario_id=user.id,modulo_id=4)
			return permiso.ver
		except Exception, e:
			return False

# Permiso para verificar si el usuario tiene permiso para editar los reportes
def puedeEditar(user):
	if user.is_superuser:
		return True
	else:
		# Modulo_id=4 pertenece a reportes
		try:
			permiso= Usuario_Modulo.objects.get(usuario_id=user.id,modulo_id=4)
			return permiso.editar
		except Exception, e:
			return False
		

@user_passes_test(puedeVisualizar,login_url='/')
def index(request):
	nombre_usuario = request.user.username.capitalize()
	boletas= Boleta.objects.all();
	lista= []
	return render(request,'reportes/index.html',{'boletas':lista,'nombre_usuario':nombre_usuario})

@login_required(login_url='/')
def exportarExcel(request):
	import xlwt
	if request.method=='POST':
		datos= json.loads(request.POST['datos'])
		response = HttpResponse(mimetype="application/ms-excel")
		response['Content-Disposition'] = 'attachment; filename=reporte.xls'
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Reporte')
		contador=0
		for d in datos['cabecera']:
			ws.write(0, contador, d)
			ws.col(contador).width= ((len(d)+10)*256)
			contador+=1

		contador=0
		filas=1

		for d in datos['cuerpo']:
			contador=0
			for a in d:
				ws.write(filas, contador, a)
				ws.col(contador).width= ((len(a)+10)*256)
				contador+=1
			filas+=1

		wb.save(response)
		return response

def procesarReporteAlmacen(request,tipo_reporte):
	tipo_filtro= request.GET['tipo_filtro']
	consulta=""
	if tipo_reporte=="general":
		inicio= request.GET['fecha_inicio']
		fin= request.GET['fecha_fin']
		if tipo_filtro=="0":
			consulta="SELECT a.identificador identificador ,COUNT(*) numero_ventas , a.nombre, SUM(b.valor_factura) valor FROM boletas_boleta b, almacenes_almacen a WHERE b.almacen_id= a.identificador AND b.fecha BETWEEN '"+inicio+" 00:00:00' AND '"+fin+" 23:59:59' GROUP BY a.nombre order by valor desc"
		else:
			consulta="SELECT c.identificador identificador ,COUNT(*) numero_ventas , c.nombre, SUM(b.valor_factura) valor FROM boletas_boleta b, almacenes_almacen a, almacenes_categoria c WHERE b.almacen_id= a.identificador AND a.categoria_id= c.identificador  AND b.fecha BETWEEN '"+inicio+" 00:00:00' AND '"+fin+" 23:59:59' GROUP BY c.nombre order by valor desc"
	else:
		campania= Campania.objects.get(pk=request.GET['campania'])
		if tipo_filtro=="0":
			consulta="SELECT a.identificador identificador ,COUNT(*) numero_ventas , a.nombre, SUM(b.valor_factura) valor FROM boletas_boleta b, almacenes_almacen a WHERE b.almacen_id= a.identificador AND b.campania_id="+str(campania.identificador)+" GROUP BY a.nombre ORDER BY valor DESC"
		else:
			consulta="SELECT c.identificador identificador ,COUNT(*) numero_ventas , c.nombre, SUM(b.valor_factura) valor FROM boletas_boleta b, almacenes_almacen a, almacenes_categoria c WHERE b.almacen_id= a.identificador AND a.categoria_id= c.identificador  AND b.campania_id="+str(campania.identificador)+" GROUP BY c.nombre ORDER BY valor DESC"

	# Recogemos todos los alamcenes, por que en dado caso de que no registren
	# ventas tiene que aparecer con un valor de ventas = 0
	almacenes= Almacen.objects.all()
	# Filtramos las boletas de acuerdo al rango de fechas proporcionadas
	lista= []
	if tipo_filtro == '0':
		boletas= Boleta.objects.raw(consulta)
		for b in boletas:
			lista.append({"id_almacen":str(b.identificador),"nombre":elimina_tildes(b.nombre),"numero_ventas":str(b.numero_ventas),"valor":str(b.valor)})
		# Ahora agregamos los almacenes que no vendieron en este periodo y se coloca un valor de 0
		for a in almacenes:
			# Recorremos la lista, si el almacen no se encuentra se agrega
			veces_encontrado=0
			for l in lista:
				if l['id_almacen'] == str(a.identificador):
					veces_encontrado+=1
			if veces_encontrado == 0:
				 lista.append({"id_almacen":str(a.identificador),"nombre":elimina_tildes(a.nombre),"numero_ventas":str(0),"valor":str(0)})

	else:
		boletas= Boleta.objects.raw(consulta);
		for b in boletas:
			lista.append({"id_categoria":str(b.identificador),"nombre":elimina_tildes(b.nombre),"numero_ventas":str(b.numero_ventas),"valor":str(b.valor)})
		# Ahora agregamos las categorias que no vendieron en este periodo y se coloca un valor de 0
		categorias= Categoria.objects.all()
		for c in categorias:
			# Recorremos la lista, si el almacen no se encuentra se agrega
			veces_encontrado=0
			for l in lista:
				if l['id_categoria'] == str(c.identificador):
					veces_encontrado+=1
			if veces_encontrado == 0:
				lista.append({"id_categoria":str(c.identificador),"nombre":elimina_tildes(c.nombre),"numero_ventas":str(0),"valor":str(0)})
	return lista

@login_required(login_url='/')
def reporteAlmacen(request):
	if request.is_ajax():
		lista=[]
		if "campania" in request.GET:
			lista=procesarReporteAlmacen(request,"campania")
		else:
			lista=procesarReporteAlmacen(request,"general")
		return HttpResponse(json.dumps(lista), mimetype='application/json')
	else:
		return HttpResponse("Peticion no valida")

# Reporte Almacen PDF

def generar_pdf(html):
    # Funcion para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

@login_required(login_url='/')
def generarReporteAlmacenPdf(request):
	lista=[]
	if "campania" in request.GET:
		lista=procesarReporteAlmacen(request,"campania")
		html = render_to_string('reportes/reporteAlmacen.html', {'pagesize':'A4', 'lista':lista,'campania':Campania.objects.get(pk=request.GET['campania'])}, context_instance=RequestContext(request))
	else:
		lista=procesarReporteAlmacen(request,"general")
		html = render_to_string('reportes/reporteAlmacen.html', {'pagesize':'A4', 'lista':lista,'fecha_inicio':request.GET['fecha_inicio'],'fecha_fin':request.GET['fecha_fin']}, context_instance=RequestContext(request))
	#return render(request,'reportes/reporteAlmacen.html',{'lista':lista})
	return generar_pdf(html)

@login_required(login_url='/')
def generarReporteCategoriaPdf(request):
	lista=[]
	if "campania" in request.GET:
		lista=procesarReporteAlmacen(request,"campania")
		html = render_to_string('reportes/reporteCategoria.html', {'pagesize':'A4', 'lista':lista,'campania':Campania.objects.get(pk=request.GET['campania'])}, context_instance=RequestContext(request))
	else:
		lista=procesarReporteAlmacen(request,"general")
		html = render_to_string('reportes/reporteCategoria.html', {'pagesize':'A4', 'lista':lista,'fecha_inicio':request.GET['fecha_inicio'],'fecha_fin':request.GET['fecha_fin']}, context_instance=RequestContext(request))
	#return render(request,'reportes/reporteAlmacen.html',{'lista':lista})
	return generar_pdf(html)

# Fin Reporte Almacen PDF

def procesarReporteCliente(request,tipo_reporte):
	clientes= Cliente.objects.all()
	consulta=""
	if tipo_reporte=="general":
		inicio= request.GET['fecha_inicio']
		fin= request.GET['fecha_fin']
		consulta="SELECT c.documento identificador, CONCAT(c.nombres,' ',c.apellidos) nombre, COUNT(*) numero_compras, SUM(b.valor_factura) valor FROM boletas_boleta b, clientes_cliente c WHERE b.cliente_id= c.id AND b.fecha BETWEEN '"+inicio+" 00:00:00' AND '"+fin+" 23:59:59' GROUP BY c.documento ORDER BY valor DESC"
	else:
		campania= Campania.objects.get(pk=request.GET['campania'])
		consulta="SELECT c.documento identificador, CONCAT(c.nombres,' ',c.apellidos) nombre, COUNT(*) numero_compras, SUM(b.valor_factura) valor FROM boletas_boleta b, clientes_cliente c WHERE b.cliente_id= c.id AND b.campania_id="+str(campania.identificador)+" GROUP BY c.documento ORDER BY valor DESC"
	lista=[]

	boletas= Boleta.objects.raw(consulta)
	
	for b in boletas:
		lista.append({"documento":str(b.identificador),"nombre":elimina_tildes(b.nombre),"numero_compras":str(b.numero_compras),"valor":str(b.valor)})
	# Ahora agregamos las clientes que no compraron en este periodo y se coloca un valor de 0
	for c in clientes:
		# Recorremos la lista, si el almacen no se encuentra se agrega
		veces_encontrado=0
		for l in lista:
			if l['documento'] == str(c.documento):
				veces_encontrado+=1
		if veces_encontrado == 0:
			lista.append({"documento":str(c.documento),"nombre":elimina_tildes(c.nombres+" "+c.apellidos),"numero_compras":str(0),"valor":str(0)})
	return lista

@login_required(login_url='/')
def reporteClientes(request):
	if request.is_ajax():
		lista=[]
		if "campania" in request.GET:
			lista= procesarReporteCliente(request,"campania")
		else:
			lista= procesarReporteCliente(request,"general")
		return HttpResponse(json.dumps(lista), mimetype='application/json')
	else:
		return HttpResponse("Peticion no valida")

# Reporte cliente pdf
@login_required(login_url='/')
def generarReporteClientePdf(request):
	if "campania" in request.GET:
		lista= procesarReporteCliente(request,"campania")
		html = render_to_string('reportes/reporteCliente.html', {'pagesize':'A4', 'lista':lista, 'campania':Campania.objects.get(pk=request.GET['campania'])}, context_instance=RequestContext(request))
	else:
		lista= procesarReporteCliente(request,"general")
		#return render(request,'reportes/reporteAlmacen.html',{'lista':lista})
		html = render_to_string('reportes/reporteCliente.html', {'pagesize':'A4', 'lista':lista,'fecha_inicio':request.GET['fecha_inicio'],'fecha_fin':request.GET['fecha_fin']}, context_instance=RequestContext(request))
	return generar_pdf(html)
# Fin reporte

@login_required(login_url='/')
def reporteDias(request):
	#if request.is_ajax():
	boletas=None
	if "campania" in request.GET:
		campania= Campania.objects.get(pk=request.GET['campania'])
		boletas= Boleta.objects.filter(campania=campania)
	else:
		inicio= request.GET['fecha_inicio']+" 00:00:00"
		fin= request.GET['fecha_fin']+" 23:59:59"
		boletas= Boleta.objects.filter(fecha__gt=inicio,fecha__lt=fin)

	lista= []
	for b in boletas:
		lista.append({'identificador':b.identificador,'dia_semana':str(b.fecha.weekday()),'hora':str(b.fecha.hour),'minutos':str(b.fecha.minute)})
	return HttpResponse(json.dumps(lista), mimetype='application/json')
	#else:
	#	return HttpResponse("Peticion no valida")

@login_required(login_url='/')
def reporteClientesEspecifico(request):
	# Clientes
	clientes= Cliente.objects.all()
	mujeres= Cliente.objects.filter(genero=False).count()
	hombres= Cliente.objects.filter(genero=True).count()
	total= mujeres+hombres
	if total>0:
		hombres=round(float(float(100*hombres)/total),2)
		mujeres=round(float(float(100*mujeres)/total),2)

	# Ciudades
	cursor = connection.cursor()
	cursor.execute('SELECT m.nombre, COUNT(*) cantidad FROM clientes_municipio m, clientes_cliente c WHERE c.ciudad_id= m.identificador GROUP BY m.nombre ORDER BY cantidad DESC LIMIT 0,6 ')
	resultado= cursor.fetchall()
	ciudades_principales=[]

	for r in resultado:
		ciudades_principales.append({'ciudad':r[0],'cantidad':r[1]})

	numero_ciudades= Municipio.objects.all()
	return render_to_response('reportes/reporteClientes.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def reporteCampanias(request):
	campanias= Campania.objects.all()
	return render_to_response('reportes/reporteCampanias.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def reporteAlmacenCampania(request):
	if request.is_ajax():
		lista=procesarReporteAlmacen(request,"campania")
		return HttpResponse(json.dumps(lista), mimetype='application/json')
	else:
		return HttpResponse("Peticion no valida")

@login_required(login_url='/')
def imprimirGrafica(request):
	titulo= request.POST['titulo']
	dic= json.loads(request.POST['datos'])
	diccionario= json.dumps(dic)
	return render_to_response('reportes/imprimir_grafica.html',locals(), context_instance=RequestContext(request))