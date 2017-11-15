from django.shortcuts import render
from django.views import generic
from .models import Student
from tutorial.models import Session

# Create your views here.
class MyBookingsList(generic.ListView):
    context_object_name = 'sessions_list'
    template_name = 'mySessions.html'

    def get_queryset(self):
        return Session.objects.filter(student__student=self.request.user)
