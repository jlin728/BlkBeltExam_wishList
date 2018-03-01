from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_item/new$', views.new),
    url(r'^add$', views.add),
    url(r'^wish_item/(?P<id>\d+)$', views.item),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),   
]