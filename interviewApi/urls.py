from django.conf.urls import url
from . import views


app_name = 'interview_api'

urlpatterns = [
    url(r'^evaluations/$', views.ListCreateEvaluation.as_view(), name='evaluations'),
    url(r'^evaluations/(?P<id>[1-9]+)/$', views.RetrieveEvaluation.as_view(), name='evaluation'),
]