from django.conf.urls import url
from . import views

app_name = 'tutors'
urlpatterns = [
    url(r'^$', views.TutorIndex.as_view(), name='tutor_index'),
    url(r'^search/$', views.search, name='tutor_search'),
    url(r'^search/results', views.SearchResults.as_view(), name='tutor_search_result'),
    url(r'^(?P<pk>[0-9]+)/$', views.ShowOneTutor.as_view(), name='tutor_detail'),
<<<<<<< HEAD
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
    url(r'^myprofile/changedetails/$', views.ChangeDetails.as_view(), name='change_details'),
    url(r'^wallet/$', views.MyWallet.as_view(), name='tutor_wallet'),
    url(r'^upcomingsessions/$', views.MySessions.as_view(), name='tutor_sessions')
=======
<<<<<<< HEAD
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
    url(r'^myprofile/changedetails/$', views.ChangeDetails.as_view(), name='change_details')
=======
    url(r'^wallet/$', views.MyWallet.as_view(), name='tutor_wallet'),
    url(r'^upcomingsessions/$', views.MySessions.as_view(), name='tutor_sessions')
>>>>>>> e75b200abe39ad4c27cf3549bd861ceb8ff8fffc
>>>>>>> b0e67cb2f561ce95cf277b066cc803954162ff92
]
