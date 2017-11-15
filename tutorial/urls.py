from django.conf.urls import url
from . import views

app_name = 'tutorial'
urlpatterns = [
    # url(r'^$', views.indexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ShowOneSession.as_view(), name='oneSession')
]
