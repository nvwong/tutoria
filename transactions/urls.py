from django.conf.urls import url
from . import views

app_name = 'transaction'
urlpatterns = [
    url(r'^add/$', views.AddMoney.as_view(), name='add'),
    url(r'^get/$', views.GetMoney.as_view(), name='get'),
]
