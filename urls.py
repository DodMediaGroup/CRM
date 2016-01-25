from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Examples:
    url(r'^$', 'views.ingresar', name='ingresar'),
    url(r'^cerrar-sesion/$', 'views.cerrarSesion', name='cerrar-sesion'),
    url(r'^crm/', include('crm.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^almacenes/', include('almacenes.urls')),
    url(r'^campanias/', include('campanias.urls')),
    url(r'^clientes/', include('clientes.urls')),
    url(r'^reportes/', include('reportes.urls')),
    url(r'^boletas/', include('boletas.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)