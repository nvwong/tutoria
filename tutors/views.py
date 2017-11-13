from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.db.models import Q
from .models import Tutor
from functools import reduce
import operator

# Create your views here.
class indexView(generic.ListView):
    model = Tutor
    context_object_name = 'tutors_list'
    template_name = 'list.html'
    def get_queryset(self):
        return Tutor.objects.all().order_by('-hourlyRate')

def search(request):
    return render_to_response('search.html')

class searchResultView(generic.ListView):
    model = Tutor
    template_name = 'searchresults.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(searchResultView, self).get_queryset()
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

        if Qlist:
            result = result.filter(reduce(operator.and_, Qlist))

        return result.order_by('-hourlyRate')

def tutors(request, tutor_id):
    return HttpResponse("Your are looking for tutor %s." % tutor_id)
