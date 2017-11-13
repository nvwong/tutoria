from django.conf.urls import url
from . import views

app_name = 'tutors'
urlpatterns = [
    url(r'^$', views.indexView.as_view(), name='index'),
    url(r'^search/$', views.search, name='tutor_search'),
    url(r'^search/results', views.searchResultView.as_view(), name='tutor_search_result'),
    url(r'^(?P<tutor_id>[0-9]+)/$', views.tutors, name='tutors')
]
