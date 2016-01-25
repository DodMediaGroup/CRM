from django.conf.urls import patterns, url
from almacenes import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^desactivar-almacen/$', views.desactivarAlmacen, name="desactivarAlmacen"),
	url(r'^agregar-almacen/$', views.agregarAlmacen, name="agregarAlmacen"),
	url(r'^agregar-categoria/$', views.agregarCategoria, name="agregarCategoria"),
	url(r'^ver-almacen/$', views.verAlmacen, name="verAlmacen"),
	url(r'^editar-almacen/$', views.editarAlmacen, name="editarAlmacen"),
	url(r'^categorias/$', views.categorias, name="categorias"),
)