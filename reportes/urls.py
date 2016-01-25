from django.conf.urls import patterns, url
from reportes import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^reporte-almacen/$', views.reporteAlmacen, name="reporteAlmacen"),
	url(r'^reporte-clientes/$', views.reporteClientes, name="reporteClientes"),
	url(r'^reporte-dias/$', views.reporteDias, name="reporteDias"),
	url(r'^generar-reporte-almacen-pdf/$', views.generarReporteAlmacenPdf, name="generarReporteAlmacenPdf"),
	url(r'^generar-reporte-categoria-pdf/$', views.generarReporteCategoriaPdf, name="generarReporteCategoriaPdf"),
	url(r'^generar-reporte-cliente-pdf/$', views.generarReporteClientePdf, name="generarReporteClientePdf"),
	url(r'^por-clientes/$', views.reporteClientesEspecifico, name="reporteClientes"),
	url(r'^por-campania/$', views.reporteCampanias, name="reporteCampanias"),

	url(r'^reporte-almacen-campania/$', views.reporteAlmacenCampania, name="reporteAlmacenCampania"),
	url(r'^exportar-excel/$', views.exportarExcel, name="exportarExcel"),
	url(r'^imprimir-grafica/$', views.imprimirGrafica, name="imprimirGrafica"),
)