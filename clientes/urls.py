from django.conf.urls import patterns, url
from clientes import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^agregar-cliente/$', views.agregar, name="agregar"),
	url(r'^ver-cliente/$', views.verCliente, name="verCliente"),
	url(r'^buscar-municipio/$', views.buscarMunicipio, name="buscarMunicipio"),
	url(r'^editar-cliente/$', views.editarCliente, name="editarCliente"),
	url(r'^editar-direccion/$', views.editarDireccion, name="editarDireccion"),
	url(r'^editar-telefono/$', views.editarTelefono, name="editarTelefono"),
	url(r'^exportar-csv/$', views.exportarCsv, name="exportarCsv"),
	url(r'^importar-archivo-csv/$', views.importarArchivoCsv, name="importarArchivoCsv"),
)