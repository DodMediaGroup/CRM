from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import *
from django.template import RequestContext
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def index(request):
	nombre_usuario = request.user.username.capitalize()
	usuarios= User.objects.filter(is_superuser=False)
	return render(request,'usuarios/index.html',{'nombre_usuario':nombre_usuario,'usuarios':usuarios})


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def agregarUsuario(request):
	if request.is_ajax():
		if request.GET['tipo']=="usuario":
			if(len(User.objects.filter(username=request.GET['username']))>0):
				return HttpResponse("True")
			else:
				return HttpResponse("False")
		if request.GET['tipo']=="correo":
			if(len(User.objects.filter(email=request.GET['correo']))>0):
				return HttpResponse("True")
			else:
				return HttpResponse("False")

	if request.method=='POST':
		nombres= request.POST['nombres']
		apellidos= request.POST['apellidos']
		correo= request.POST['correo']
		password= request.POST['password']
		username= request.POST['username']
		grupo= Group.objects.get(pk=request.POST['grupo'])
		rePassword= request.POST['confirmPassword']
		if password == rePassword:
			user = User.objects.create_user(username, correo, password)
			user.first_name= nombres
			user.last_name= apellidos
			try:
				user.save()
				grupo.user_set.add(user)
				mensaje_exito="Usuario agregado exitosamente."
			except Exception, e:
				mensaje_error="No se pudo agregar el usuario. Es posible que el nombre de usuario ya se encuentre registrado"
	
	grupos= Group.objects.all()
	return render_to_response('usuarios/agregar.html',locals(), context_instance=RequestContext(request))

@login_required(login_url="/")
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def desactivarUsuario(request):
	if request.is_ajax():
		try:
			usuario= User.objects.get(pk=request.GET['id_usuario'])
			usuario.is_active= not usuario.is_active
			usuario.save()
			if usuario.is_active:
				return HttpResponse("Activo")
			else:
				return HttpResponse("Inactivo")
		except Exception, e:
			return HttpResponse("No se logro realizar la operacion")
	else:
		return HttpResponse('Peticion no valida')

@login_required(login_url="/")
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def editarUsuario(request):
	usuario= User.objects.get(id=request.GET['id'])
	if request.method=="POST":
		grupo= Group.objects.get(pk=request.POST['grupo'])
		usuario.first_name= request.POST['nombres']
		usuario.last_name= request.POST['apellidos']
		usuario.email= request.POST['correo']
		usuario.save()
		usuario.groups.clear()
		grupo.user_set.add(usuario)
		mensaje_exito="Se ha actualizado la informacion"
	grupos= Group.objects.all()
	g_usuario= Group.objects.get(user=usuario)
	return render_to_response('usuarios/editar.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def cambiarContrasenia(request):
	usuario= User.objects.get(pk=request.user.pk)
	if request.method== "POST":
		pass1= request.POST['password']
		pass2= request.POST['confirmPassword']
		if pass1==pass2:
			if usuario.check_password(request.POST['actual']):
				usuario.set_password(pass1)
				mensaje_exito="informacion actualizada"
			else:
				mensaje_error="Error en la actualizacion las claves no coinciden"
	return render_to_response('usuarios/cambiar_clave.html',locals(), context_instance=RequestContext(request))


