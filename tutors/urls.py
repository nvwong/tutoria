from django.conf.urls import url
from . import views

app_name = 'tutors'
urlpatterns = [
    url(r'^$', views.indexView.as_view(), name='index'),
    url(r'^(?P<tutor_id>[0-9]+)/$', views.tutors, name='tutors')
]
