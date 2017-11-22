from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.db.models import Q
from .models import Tutor, NotAvailableSlot
from functools import reduce
from tutorial.models import Session
import operator

# Create your views here.
class TutorIndex(generic.ListView):
    model = Tutor
    context_object_name = 'tutors_list'
    template_name = 'list.html'
    def get_queryset(self):
        return Tutor.objects.all().order_by('-hourlyRate')

def search(request):
    return render_to_response('search.html')

class MyProfile(generic.ListView):
    model = Tutor
    context_object_name = 'myProfile'
    template_name = 'myTutorProfile.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyProfile, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

class ChangeDetails(generic.ListView):
    model = Tutor
    context_object_name = 'myProfile'
    template_name = 'changeTutorDetails.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ChangeDetails, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

class SearchResults(generic.ListView):
    model = Tutor
    template_name = 'searchresults.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(SearchResults, self).get_queryset()
        result = Tutor.objects.all()

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
            Qlist.append(Q(hourlyRate__lte=hourlyrate))
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
    context_object_name = 'sessions_list'
    template_name = 'upcomingsessions.html'

    def get_queryset(self):
        session = Session.objects.filter(tutor__tutor=self.request.user)
        upcoming = session.filter(isLocked=False)
        return upcoming

class MyWallet(generic.ListView):
    model = Session
    context_object_name = 'sessions_list'
    template_name = 'wallet.html'

    def get_queryset(self):
        session = Session.objects.filter(tutor__tutor=self.request.user)
        trans_history = session.filter(isLocked=True)
        return trans_history

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyWallet, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

