from django.conf.urls import url
from . import views

app_name = 'students'
urlpatterns = [
    # url(r'^$', views.indexView.as_view(), name='index'),
    url(r'^my/$', views.MyBookingsList.as_view(), name='mybookings')
]
