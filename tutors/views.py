from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.db.models import Q
from .models import Tutor, NotAvailableSlot
from functools import reduce
from tutorial.models import Session
from transactions.models import Transaction, Wallet
import operator
from .models import User
#from django.contrib.auth.models import User
from .models import NotAvailableSlot
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.
class TutorIndex(generic.ListView):
    model = Tutor
    context_object_name = 'tutors_list'
    template_name = 'list.html'
    def get_queryset(self):
        return Tutor.objects.filter(show_tutor=True).order_by('-hourlyRate')

def search(request):
    return render(request, 'search.html')

class MyProfile(generic.ListView):
    model = Tutor
    context_object_name = 'myProfile'
    template_name = 'myTutorProfile.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyProfile, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        context['unavailability_list'] = NotAvailableSlot.objects.filter(tutor__tutor=self.request.user)
        return context

class UnavailabilityList (generic.ListView):
    model = NotAvailableSlot
    context_object_name = 'unavailability_list'
    template_name = 'slots_list.html'

    def get_queryset(self):
        return NotAvailableSlot.objects.filter(tutor__tutor=self.request.user)

def cancel_slot(request):
    try:
        selected_slot = NotAvailableSlot.objects.get(pk=request.POST['choice'])
    except (KeyError, NotAvailableSlot.DoesNotExist):
        # Redisplay the session voting form.
        return render(request, 'slots_list.html', {'error_message': "You didn't select a slot.",})
    else:
        selected_slot.delete()
        return render(request,'cancelok.html')

class ChangePhoneNumber(SuccessMessageMixin,UpdateView):
    model = Tutor
    fields = ['avatar','privateTutor','phoneNumber', 'timePerSlot','university', 'introduction','show_tutor','courseTaught','tags']
    template_name = 'changeTutorPhoneNumber.html'
    success_message = 'Successfully saved!!!!'
    success_url = reverse_lazy('tutors:myprofile')

    def get_object(self, **kwargs):
        return Tutor.objects.get(tutor__username=self.request.user.username)

class ChangeHourlyRate(SuccessMessageMixin,UpdateView):
    model = Tutor
    fields = ['hourlyRate']
    template_name = 'changeHourlyRate.html'
    success_message = 'Successfully saved!!!!'
    success_url = reverse_lazy('tutors:myprofile')

    def get_object(self, **kwargs):
        return Tutor.objects.get(tutor__username=self.request.user.username)

class ChangeAvailability(SuccessMessageMixin,generic.CreateView):
    model = NotAvailableSlot
    fields = ['start_time', 'end_time']
    template_name = 'changeAvailability.html'
    success_message = 'Successfully added!!!!'
    success_url = reverse_lazy('tutors:myprofile')

    def form_valid(self, form):
        the_tutor = Tutor.objects.get(tutor=self.request.user)
        form.instance.tutor = the_tutor
        return super(ChangeAvailability, self).form_valid(form)

class ChangeUserdetail(SuccessMessageMixin,UpdateView):
    model = User
    fields = ['last_name', 'first_name', 'email']
    template_name = 'changeTutorUserdetail.html'
    success_message = 'Successfully saved!!!!'
    success_url = reverse_lazy('tutors:myprofile')

    def get_object(self, **kwargs):
        return User.objects.get(id=self.request.user.id)

class SearchResults(generic.ListView):
    model = Tutor
    template_name = 'searchresults.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(SearchResults, self).get_queryset()
        result = Tutor.objects.filter(show_tutor=True)

        tname = self.request.GET.get('tname')
        uni = self.request.GET.get('university')
        courses = self.request.GET.get('course')
        tag = self.request.GET.get('tags')
        hourlyrate = self.request.GET.get('hourlyrate')
        private = self.request.GET.get('privateornot')
        Qlist = []
        if tname:
            name_words = tname.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(tutor__first_name__icontains=name) for name in name_words)) |
                reduce(operator.and_,
                       (Q(tutor__last_name__icontains=name) for name in name_words))
            )
        if uni:
            Qlist.append(Q(university__icontains=uni))
        if courses:
            Qlist.append(Q(courseTaught__course_code__icontains=courses))
        if tag:
            Qlist.append(Q(tags__tag_name__icontains=tag))
        if hourlyrate:
            Qlist.append(Q(hourlyRate=hourlyrate))
            Qlist.append(Q(privateTutor=True))
        if private:
            Qlist.append(Q(privateTutor=True))
        if not (private):
            Qlist.append(Q(privateTutor=False))

        if Qlist:
            result = result.filter(reduce(operator.and_, Qlist))

        return result.order_by('-hourlyRate')

class ShowOneTutor(generic.DetailView):
    model = Tutor
    template_name = 'viewOneTutor.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ShowOneTutor, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['unavailability_list'] = NotAvailableSlot.objects.all()
        return context

class MySessions(generic.ListView):
    model = Session
    context_object_name = 'sessions_list'
    template_name = 'upcomingsessions.html'

    def get_queryset(self):
        session = Session.objects.filter(tutor__tutor=self.request.user)
        # upcoming = session.filter(isLocked=False)
        return session

class MyWallet(generic.ListView):
    model = Transaction
    context_object_name = 'transactions_list'
    template_name = 'wallet.html'

    def get_queryset(self):
        earliest = timezone.now() - timezone.timedelta(days=30)
        return Transaction.objects.filter(owner=self.request.user).filter(timestamp__gte=earliest).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(MyWallet, self).get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(owner=self.request.user)
        return context
