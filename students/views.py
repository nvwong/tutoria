from django.shortcuts import render
from django.views import generic
from tutorial.models import Session, Review
from tutors.models import Tutor
from .models import Student
from datetime import date, time, datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User
from tutors.models import Tutor
from transactions.models import Transaction, Wallet
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime, timedelta
from django.utils import timezone

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

class ChangeDetails(generic.ListView):
    model = Student
    context_object_name = 'myProfile'
    template_name = 'changeDetails.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ChangeDetails, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

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
        new_review = Review(session=session)
    except (KeyError, Session.DoesNotExist):
            # Redisplay the session voting form.
            return render(request, 'review_form.html', {'error_message': "You didn't select a session.",})
    else:
        session.reviewed=True
        rate_time = session.tutor.rate_time
        real_rating = session.tutor.rating
        real_rating = (real_rating*rate_time + int(rating))/(rate_time+1)
        session.tutor.rate_time += 1
        new_review.time_review = timezone.now()
        session.save()
        new_review.save()
        session.tutor.save()
        return render(request,'review_ok.html')
        #HttpResponseRedirect(reverse('students:reviewok', args=()))

class MyWallet(generic.ListView):
    model = Transaction
    context_object_name = 'transactions_list'
    template_name = 'mywallet.html'

    def get_queryset(self):
        earliest = timezone.now() - timezone.timedelta(days=30)
        return Transaction.objects.filter(owner=self.request.user).filter(timestamp__gte=earliest).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(MyWallet, self).get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(owner=self.request.user)
        return context
