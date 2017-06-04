from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="reg"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^add$', views.add, name='add'),
    url(r'^process$', views.process, name='process'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^delete_trip/(?P<id>\d+)$', views.delete_trip, name='delete_trip'),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip, name='join_trip'),
]
