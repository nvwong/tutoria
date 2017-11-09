from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .models import Session

# Create your views here.
class oneSessionView(generic.DetailView):
    model = Session
    template_name = 'oneSession.html'
