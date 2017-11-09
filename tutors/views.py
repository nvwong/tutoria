from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .models import Tutor

# Create your views here.
class indexView(generic.ListView):
    model = Tutor
    context_object_name = 'tutors_list'
    template_name = 'list.html'
    def get_queryset(self):
        return Tutor.objects.all().order_by('-hourly_rate')

def tutors(request, tutor_id):
    return HttpResponse("Your are looking for tutor %s." % tutor_id)
