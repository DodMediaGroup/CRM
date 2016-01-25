from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from clientes.models import Cliente, Departamento
from almacenes.models import Almacen
from campanias.models import CampaniaAlmacen
from campanias.models import Campania
from django.core import serializers
from boletas.models import Boleta
from django.http import Http404
# Librerias necesarias para generar un pdf
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.template import RequestContext

def formatear_fecha(fecha):
	dias_semana= ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
	meses= ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
	return dias_semana[int(str(fecha.weekday))]+", "+fecha.day+" de "+meses[int(str(fecha.month))]+" del "+fecha.year

@login_required(login_url='/')
@user_passes_test(lambda u: "boletas.view_boleta" in u.get_all_permissions(), login_url='/')
def index(request):
	#Recopilamos las campanias activas
	campanias= Campania.objects.filter(estado=1)
	boleta_campania=[]
	for c in campanias:
		numero_boletas= len(Boleta.objects.filter(campania_id=c.identificador))
		boleta_campania.append({'campania':c,'cantidad':numero_boletas})
	return render(request,'boletas/index.html',{'campanias':campanias,'boleta_campania':boleta_campania})

@login_required(login_url='/')
@user_passes_test(lambda u: "clientes.add_cliente" in u.get_all_permissions(), login_url='/')
def registroCliente(request):
	if request.method =='POST':
		documento= request.POST['documento']
		#obtenemos ahora la campania a la que se va a registrar la factura
		#independientemente del registro del cliente
		campania_id= request.POST['campania']
		#Ahora buscamos los almacenes que hacer parte de la campania seleccionada
		campania= Campania.objects.get(pk=campania_id)
		campania_almacen= CampaniaAlmacen.objects.filter(campania_id=campania_id,participa=1)
		almacen= Almacen.objects.get(pk=request.POST['almacen'])
		#ahora se busca en la base de datos si se encuentra registrado o no
		try:
			#Esto en caso de la opcion de que al verificar el documento si se 
			#encuentre el cliente
			cliente= Cliente.objects.get(documento=documento)
			#Si todo marcha a la perfeccion procedemos a agregar la factura como paso final
			return render(request, 'boletas/agregarFactura.html',{'campania':campania,'cliente':cliente,'almacen':almacen,'campania_almacen':campania_almacen})
		except Exception, e:
			#si no se encuentra, entonces quiere decir que se va a agregar
			#Por tanto recolectamos todos los datos
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
			if observaciones == "":
				observaciones = "Ninguna"
			var= fecha_nacimiento.split('/')
			#para la fecha, tenemos que trasformarla en el formato que mysql recibe
			fecha_nacimiento= var[2]+"-"+var[0]+'-'+var[1]
			departamentos= Departamento.objects.all()
			nombre_usuario = request.user.username.capitalize()
			try:
				cliente= Cliente(documento,tipo_doc,nombres,apellidos,genero,fecha_nacimiento,estado_civil,telefono,correo,direccion,ciudad,observaciones)
				cliente.save()
				#Si todo marcha a la perfeccion procedemos a agregar la factura como paso final
				return render(request, 'boletas/agregarFactura.html',{'campania':campania,'cliente':cliente,'campania_almacen':campania_almacen})				
			except Exception, e:
				raise e
				return render(request,'boletas/registroCliente.html',{'mensaje_error':'No se logro completar la operacion. Favor verifique sus datos','campania':campania,'departamentos':departamentos})
	else:
		# Vista normal. para acceder es necesario venir con el id de la campania
		try:
			departamentos= Departamento.objects.all()
			campania=Campania.objects.get(pk=request.GET['id_campania'])
			campania_almacen= CampaniaAlmacen.objects.filter(campania_id=campania.identificador,participa=1)
			return render(request,'boletas/registroCliente.html',{'campania':campania,'departamentos':departamentos,'campania_almacen':campania_almacen})
		except Exception, e:
			raise Http404("El contenido solicitado no existe")

@login_required(login_url='/')
def buscarDocumento(request):
	if request.is_ajax():
		# Se busca con .filter con el fin de poder serializar el objto
		cliente= Cliente.objects.filter(documento=request.GET['documento'], tipo_documento=request.GET['tipo_doc']);
		data = serializers.serialize('json',cliente)
		return HttpResponse(data, mimetype='application/json')
	else:
		return HttpResponse('Peticion no valida')

@login_required(login_url='/')
@user_passes_test(lambda u: "boletas.add_boleta" in u.get_all_permissions(), login_url='/')
def almacenarFactura(request):
	if request.method=="POST":
		boleta= Boleta()
		var= request.POST['fecha'].split('/')
		boleta.fecha = var[2]+"-"+var[0]+'-'+var[1]+' '
		boleta.fecha += request.POST['hora']+':00'	
		boleta.valor_factura= request.POST['valor_boleta']
		try:
			boleta.campania= Campania.objects.get(pk=request.POST['campania_hidden'])
			boleta.almacen= Almacen.objects.get(pk=request.POST['almacen_hidden'])
			boleta.cliente= Cliente.objects.get(documento=request.POST['cliente_hidden'])
			boleta.save()
			
			return render(request,'boletas/verBoleta.html',{'boleta':boleta})
			# A partir de aqui se genera un pdf con las boletas que le corresponden
			#response = HttpResponse(content_type='application/pdf')
			#response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

			# Create the PDF object, using the response object as its "file."
			#p = canvas.Canvas(response)

			# Draw things on the PDF. Here's where the PDF generation happens.
			# See the ReportLab documentation for the full list of functionality.
			#p.drawString(100, 100, "Hello world.")

			# Close the PDF object cleanly, and we're done.
			#p.showPage()
			#p.save()
			#return response
		except Exception, e:
			raise e
	else:
		return render(request,'boletas/almacenarFactura.html')

@login_required(login_url='/')
@user_passes_test(lambda u: "boletas.view_boleta" in u.get_all_permissions(), login_url='/')
def verBoletas(request):
	boletas= Boleta.objects.all()
	return render(request,'boletas/verBoletas.html',{'boletas':boletas})

@login_required(login_url='/')
@user_passes_test(lambda u: "boletas.view_boleta" in u.get_all_permissions(), login_url='/')
def verBoleta(request):
	try:
		boleta= Boleta.objects.get(pk=request.GET['id'])
		return render(request,'boletas/verBoleta.html',{'boleta':boleta})
	except Exception, e:
		raise Http404("El contenido solicitado no existe")


def generar_pdf(html):
    # Funcion para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def generarBoleta(request):
	# vista de ejemplo con un hipotetico modelo Libro
	boleta= Boleta.objects.get(pk=request.GET['id'])
	numero_boletas= boleta.valor_factura/boleta.campania.valor_boleta
	lista= []
	for n in range(numero_boletas):
		lista.append(boleta)
	#return render(request,'boletas/reporte.html',{'lista':lista,'numero_boletas':numero_boletas})
	html = render_to_string('boletas/reporte.html', {'pagesize':'A4', 'lista':lista, 'numero_boletas':numero_boletas}, context_instance=RequestContext(request))
	return generar_pdf(html)