from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^createprospect', views.createpros),
    url(r'^dashboard$', views.dashboard),
    url(r'^prospects/(?P<id>\d+)$', views.prospect),
    url(r'^prospects/(?P<id>\d+)/notes$', views.note),

]