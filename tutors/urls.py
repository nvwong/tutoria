from django.conf.urls import url
from . import views

app_name = 'tutors'
urlpatterns = [
    url(r'^$', views.TutorIndex.as_view(), name='tutor_index'),
    url(r'^search/$', views.search, name='tutor_search'),
    url(r'^search/results', views.SearchResults.as_view(), name='tutor_search_result'),
    url(r'^(?P<pk>[0-9]+)/$', views.ShowOneTutor.as_view(), name='tutor_detail'),
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
    url(r'^myprofile/changephonenumber/$', views.ChangePhoneNumber.as_view(success_url="/"), name='change_phonenumber'),
    url(r'^myprofile/changeavailability/$', views.ChangeAvailability.as_view(success_url="/"), name='change_availability'),
    url(r'^myprofile/changeuserdetail/$', views.ChangeUserdetail.as_view(success_url="/"), name='change_userdetail'),
    url(r'^myprofile/changehourlyrate/$', views.ChangeHourlyRate.as_view(success_url="/"), name='change_hourlyrate'),
    url(r'^wallet/$', views.MyWallet.as_view(), name='tutor_wallet'),
    url(r'^upcomingsessions/$', views.MySessions.as_view(), name='tutor_sessions')
]
