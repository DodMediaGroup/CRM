from django.conf.urls import patterns, url
from boletas import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^buscar-documento/$', views.buscarDocumento, name="buscarDocumento"),
	url(r'^registro-cliente/$', views.registroCliente, name="registroCliente"),
	url(r'^almacenar-factura/$', views.almacenarFactura, name="almacenarFactura"),
	url(r'^ver-boletas/$', views.verBoletas, name="verBoletas"),
	url(r'^ver-boleta/$', views.verBoleta, name="verBoleta"),
	url(r'^generar-boleta/$', views.generarBoleta, name="generarBoleta"),
)