from django.conf.urls import url
from . import views

app_name = 'students'
urlpatterns = [

    url(r'^my/$', views.MyBookingsList.as_view(), name='mybookings'),
    url(r'^review/$', views.ReviewList.as_view(), name='review_list'),
    url(r'^review/(?P<pk>[0-9]+)/$', views.ReviewForm.as_view(), name='review_form'),
    url(r'^review/(?P<pk>[0-9]+)/make/$', views.saveReview, name='save_review'),
    url(r'^myprofile/$', views.MyProfile.as_view(), name='myprofile'),
<<<<<<< HEAD
    url(r'^myprofile/changephonenumber/$', views.ChangePhoneNumber.as_view(success_url="/"), name='change_phonenumber'),
        url(r'^myprofile/changeuserdetail/$', views.ChangeUserdetail.as_view(success_url="/"), name='change_userdetail'),
=======
    url(r'^myprofile/changedetails/$', views.ChangeDetails.as_view(), name='change_details'),
>>>>>>> bacf986d8220ccf81ea2df34d4af9357490e2d0e
    url(r'^wallet/$', views.MyWallet.as_view(), name='student_wallet'),

    #url(r'^review/ok/$',views.
]
