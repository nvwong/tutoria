from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tutors.models import Tutor
from students.models import Student


class TutorRegistrationForm(UserCreationForm):
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
        model = Tutor
        fields = ('username', 'email', 'password', 'phone_number', 'designed_name', 'university', 'course_code', 'tage', 'hourly_rate', 'introduction')

    def save(self, commit=True):
        Tutor = super(TutorRegistrationForm, self).save(commit=False)
        Tutor.username = self.cleaned_data['username']
        Tutor.password = self.cleaned_data['password']
        Tutor.email = self.cleaned_data['email']
        Tutor.designed_name = self.cleaned_data['designed_name']
        Tutor.phone_number = self.cleaned_data['phone_number']
        Tutor.university = self.cleaned_data['university']
        Tutor.course_code = self.cleaned_data['course_code']
        Tutor.tag = self.cleaned_data['tag']
        Tutor.hourly_rate = self.cleaned_data['hourly_rate']
        Tutor.introduction = self.cleaned_data['introduction']

        if commit:
            Tutor.save()

        return Tutor


class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField(required=True)
    designed_name = forms.CharField(required=True)


    class Meta:
        model = Student
        fields = ('username', 'email', 'password', 'phone_number', 'designed_name')

    def save(self, commit=True):
        Student = super(StudentRegistrationForm, self).save(commit=False)
        Student.username = self.cleaned_data['username']
        Student.password = self.cleaned_data['password']
        Student.email = self.cleaned_data['email']
        Student.designed_name = self.cleaned_data['designed_name']
        Student.phone_number = self.cleaned_data['phone_number']

        if commit:
            Student.save()

        return Student
