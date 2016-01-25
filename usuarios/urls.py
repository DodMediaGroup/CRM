from django.conf.urls import patterns, url
from usuarios import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^agregar-usuario/$', views.agregarUsuario, name="agregarUsuario"),
	url(r'^editar-usuario/$', views.editarUsuario, name="editarUsuario"),
	#vistas ajax
	url(r'^desactivar-usuario/$', views.desactivarUsuario, name="desactivarUsuario"),
	url(r'^cambiar-contrasenia/$', views.cambiarContrasenia, name="cambiarContrasenia"),
)