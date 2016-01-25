from django.conf.urls import patterns, url
from campanias import views

urlpatterns = patterns('',
	#urls de compras
	url(r'^$', views.index, name="index"),
	url(r'^agregar-campanias/$', views.agregarCampania, name="agregarCampania"),
	url(r'^desactivar-campania/$', views.desactivarCampania, name="desactivarCampania"),
	url(r'^editar-almacenes-campania/$', views.editarAlmacenesCampania, name="editarAlmacenesCampania"),
	url(r'^editar-participacion/$', views.editarParticipacion, name="editarParticipacion"),
	url(r'^ver_campania/$', views.verCampania, name="verCampania"),
	url(r'^editar-campania/$', views.editarCampania, name="editarCampania"),
)