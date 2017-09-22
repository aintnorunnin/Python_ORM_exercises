from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^display$', views.display),
    url(r'^check$', views.check),
    url(r'^clear$', views.clear),
]
