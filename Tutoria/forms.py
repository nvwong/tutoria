from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentSignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=True)
    phone_number = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'avatar', 'first_name', 'last_name', 'email', 'phone_number')

class TutorSignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=True)
    phoneNumber = forms.CharField(required=True)
    privateTutor = forms.BooleanField(required=False)
    university = forms.CharField(required=True)
    #course_code = forms.CharField(required=True)
    hourly_rate = forms.IntegerField(required=True, help_text='Contracted Tutor please input 0')
    introduction = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'avatar', 'first_name', 'last_name', 'email', 'privateTutor', 'phoneNumber', 'university', 'hourly_rate', 'introduction')
