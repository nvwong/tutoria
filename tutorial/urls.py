from django.conf.urls import url
from . import views

app_name = 'tutorial'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.ShowOneSession.as_view(), name='oneSession'),
    url(r'^cancel/$', views.sessionListView.as_view(), name='session_list'),
    url(r'^cancel/make_a_cancel/$', views.cancel, name='make_cancel'),
    url(r'^book/(?P<tutor_id>[0-9]+)/', views.MakeBooking.as_view(), name='make_booking'),
    # url(r'^$', views.indexView.as_view(), name='index'),
]
