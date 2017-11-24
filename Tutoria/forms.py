from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MyRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField(required=True)
    designed_name = forms.CharField(required=True)
    university = forms.CharField(required=True)
    course_code = forms.CharField(required=True)
    tag = forms.CharField(required=True)
    hourly_rate = forms.IntegerField(required=True)
    introduction = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number', 'designed_name', 'university', 'course_code', 'tage', 'hourly_rate', 'introduction')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        user.email = self.cleaned_data['email']
        user.designed_name = self.cleaned_data['designed_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.university = self.cleaned_data['university']
        user.course_code = self.cleaned_data['course_code']
        user.tag = self.cleaned_data['tag']
        user.hourly_rate = self.cleaned_data['hourly_rate']
        user.introduction = self.cleaned_data['introduction']

        if commit:
            user.save()

        return user
