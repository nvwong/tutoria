from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

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
    return render(request, 'registration\signup.html', {'form': form})

def start(request):
    if request.user.groups.filter(name='student').count():
        return render(request, '/tutors/search/',) #student index page
    if request.user.groups.filter(name='tutor').count():
        return render(request, '/tutors/wallet/',) #tutor index page
