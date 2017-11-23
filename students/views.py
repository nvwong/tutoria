from django.shortcuts import render
from django.views import generic
from tutorial.models import Session, Review
from tutors.models import Tutor
from .models import Student
from .models import User
from datetime import date, time, datetime
from students.models import Student
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#from django.core.mail import EmailMessage
from tutors.models import Tutor
from students.models import Student
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
class MyBookingsList(generic.ListView):
    context_object_name = 'sessions_list'
    template_name = 'mySessions.html'

    def get_queryset(self):
        return Session.objects.filter(student__student=self.request.user)

class MyProfile(generic.ListView):
    model = Student
    context_object_name = 'myProfile'
    template_name = 'myProfile.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyProfile, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

class ChangePhoneNumber(SuccessMessageMixin,UpdateView):
    model = Student
    fields = ['avatar','phone_number']
    template_name = 'changePhoneNumber.html'
    template_name_suffix = '_update_form'
    success_message = 'List successfully saved!!!!'

    def get_object(self, **kwargs):
        return Student.objects.get(student__username=self.request.user.username)

class ChangeUserdetail(SuccessMessageMixin,UpdateView):
    model = User
    fields = ['last_name', 'first_name', 'email']
    template_name = 'changeUserdetail.html'
    template_name_suffix = '_update_form'
    success_message = 'List successfully saved!!!!'

    def get_object(self, **kwargs):
        return User.objects.get(id=self.request.user.id)

class ReviewList(generic.ListView):
    model = Session
    template_name = 'review_list.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        student = self.request.user
        username = student.username
        session = Session.objects.filter(student__student__username=username)
        need_review = session.filter(isLocked=True).filter(reviewed=False)
        return need_review


class ReviewForm(generic.DetailView):
    model = Session
    template_name = 'review_form.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewForm, self).get_context_data(**kwargs)
        #If you dont call 'super', you wont have the context processor varibles
        #  like 'user'
        context['user'] = self.request.user # you can add template variables!
        session_id = self.kwargs['pk']
        context['session_id'] = session_id
        return context

def saveReview(request, pk):
    try:
        rating = request.POST['rating']
        content = request.POST['review']
        session = Session.objects.get(id=pk)
    except (KeyError, Session.DoesNotExist):
            # Redisplay the session voting form.
            return render(request, 'review_form.html', {'error_message': "You didn't select a session.",})
    else:
        session.reviewed=True
        rate_time = session.tutor.rate_time
        real_rating = session.review.rating
        real_rating = (real_rating*rate_time + int(rating))/(rate_time+1)
        rate_time+=1
        session.review.time_review = datetime.now()
        session.save()
        return render(request,'review_ok.html')
        #HttpResponseRedirect(reverse('students:reviewok', args=()))

class MyWallet(generic.ListView):
    model = Session
    context_object_name = 'sessions_list'
    template_name = 'mywallet.html'

    def get_queryset(self):
        session = Session.objects.filter(student__student=self.request.user)
        trans_history = session.filter(isLocked=True)
        return trans_history

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyWallet, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context
