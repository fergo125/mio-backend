from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^tides/(?P<pk>[0-9]+)/week$', views.TideWeek.as_view(),name='tides-week'),

]
#Esto permite que el servidor reciva indicaciones con sufijos segun el tipo de datos que se quiera obtener
urlpatterns = format_suffix_patterns(urlpatterns)
