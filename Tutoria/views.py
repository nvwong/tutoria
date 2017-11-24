from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from tutors.models import Tutor
from students.models import Student
from django.views import generic
from .forms import TutorRegistrationForm, StudentRegistrationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tutors/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def signup_tutor(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tutors/')
    else:
        form = TutorRegistrationForm()
    return render(request, 'registration/signup_tutor.html', {'form': form})



def signup_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tutors/')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/signup_student.html', {'form': form})


@login_required
def start(request):
    uid = request.user.id
    user = User.objects.get(pk=request.user.id)
    if user.groups.filter(name='Student').exists():
        template = 'index'#'search.html' #student index page
    if user.groups.filter(name='Tutor').exists():
        template = 'index_tutor'
    return HttpResponseRedirect(reverse(template)) #tutor index page
