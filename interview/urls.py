from django.conf.urls import url
from . import views

app_name='interview'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^list/$', views.list, name="list"),
]