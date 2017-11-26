from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from tutors.models import Tutor
from students.models import Student
from .forms import TutorSignUpForm, StudentSignUpForm
from django.views import generic
from django.contrib.auth.models import Group

def signup(request):
    return render(request, 'registration/signup.html', {})

def signup_tutor(request):
    if request.method == 'POST':
        form = TutorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.tutor.phoneNumber = form.cleaned_data.get('phoneNumber')
            user.tutor.privateTutor = form.cleaned_data.get('privateTutor')
            user.tutor.university = form.cleaned_data.get('university')
            user.tutor.hourlyRate = form.cleaned_data.get('hourly_rate')
            user.tutor.introduction = form.cleaned_data.get('introduction')
            user.tutor.avatar = form.cleaned_data['avatar']
            g = Group.objects.get(name='Tutor')
            g.user_set.add(user)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = TutorSignUpForm()
    return render(request, 'registration/signup_tutor.html', {'form': form})



def signup_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.student.phone_number = form.cleaned_data.get('phone_number')
            user.student.avatar = form.cleaned_data['avatar']
            g = Group.objects.get(name='Student')
            g.user_set.add(user)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/signup_student.html', {'form': form})

@login_required
def start(request):
    uid = request.user.id
    user = User.objects.get(pk=request.user.id)
    template = 'index'
    if user.groups.filter(name='Student').exists():
        template = 'index' #'search.html' #student index page
    if user.groups.filter(name='Tutor').exists():
        template = 'index_tutor'
    return HttpResponseRedirect(reverse(template)) #tutor index page
