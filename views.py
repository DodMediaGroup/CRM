import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response

def ingresar(request):
	if request.user.is_authenticated():
		return redirect('crm.views.index')
	else:
		if request.method == 'POST':
			username = request.POST['usuario']
			password = request.POST['contrasenia']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					if user.is_superuser:
						return redirect('crm.views.index')
					else:
						#return redirect('login.views.indexUsuario')
						return redirect('crm.views.index')
				else:
					return render(request, 'home/home.html', {'mensaje_error':"El usuario no se encuentra activo"})
			else:
				return render(request, 'home/home.html', {'mensaje_error':"Usuario y clave no coinciden"})
		else:
			return render(request, 'home/home.html')

def cerrarSesion(request):
	logout(request)
	return redirect('openshift.views.ingresar')
