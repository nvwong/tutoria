from django.conf.urls import url
from . import views

app_name = 'students'
urlpatterns = [

    url(r'^my/$', views.MyBookingsList.as_view(), name='mybookings'),
    url(r'^review/$', views.ReviewList.as_view(), name='review_list'),
    url(r'^review/(?P<pk>[0-9]+)/$', views.ReviewForm.as_view(), name='review_form'),
    url(r'^review/(?P<pk>[0-9]+)/make/$', views.saveReview, name='save_review'),
<<<<<<< HEAD
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
    url(r'^myprofile/changedetails/$', views.ChangeDetails.as_view(), name='change_details'),
    url(r'^wallet/$', views.MyWallet.as_view(), name='student_wallet')
=======
<<<<<<< HEAD
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
    url(r'^myprofile/changedetails/$', views.ChangeDetails.as_view(), name='change_details'),
=======
    url(r'^wallet/$', views.MyWallet.as_view(), name='student_wallet'),
>>>>>>> e75b200abe39ad4c27cf3549bd861ceb8ff8fffc
>>>>>>> b0e67cb2f561ce95cf277b066cc803954162ff92
    #url(r'^review/ok/$',views.
]
