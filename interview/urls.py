from django.conf.urls import url
from . import views

app_name='interview'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^retrieve/(?P<id>[0-9]+)/$', views.retrieve, name='retrieve'),
]