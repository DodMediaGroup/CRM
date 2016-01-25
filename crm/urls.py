from django.conf.urls import patterns, url
from crm import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^generar_reporte_clientes/$', views.generarReporteClientes, name="generarReporteClientes"),
)