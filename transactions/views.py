from django.shortcuts import render
from django.views import generic
from .models import Transaction
from students.models import Student
from tutors.models import Tutor
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class AddMoney (SuccessMessageMixin, generic.CreateView):
    model = Transaction
    fields = ['amount']
    template_name = "addmoney.html"
    success_message = 'Adding Money Successful.'
    success_url = reverse_lazy('transaction:add')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.timestamp = timezone.now()
        self.object = form.save()
        if (Student.objects.filter(student=self.request.user).exists()):
            stu = Student.objects.get(student=self.request.user)
            stu.wallet += form.instance.amount
            stu.save()
        elif (Tutor.objects.filter(tutor=self.request.user).exists()):
            tut = Tutor.objects.get(tutor=self.request.user)
            tut.wallet += form.instance.amount
            tut.save()
        return super(AddMoney, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddMoney, self).get_context_data(**kwargs)
        if (Student.objects.filter(student=self.request.user).exists()):
            context['logged_user'] = Student.objects.get(student=self.request.user)
        elif (Tutor.objects.filter(tutor=self.request.user).exists()):
            context['logged_user'] = Tutor.objects.get(tutor=self.request.user)
        return context

class GetMoney (SuccessMessageMixin, generic.CreateView):
    model = Transaction
    fields = ['amount']
    template_name = "getmoney.html"
    success_message = 'Getting Money Successful.'
    success_url = reverse_lazy('transaction:get')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.timestamp = timezone.now()
        form.instance.amount = -(form.instance.amount)
        self.object = form.save()
        if (Student.objects.filter(student=self.request.user).exists()):
            stu = Student.objects.get(student=self.request.user)
            stu.wallet += form.instance.amount
            stu.save()
        elif (Tutor.objects.filter(tutor=self.request.user).exists()):
            tut = Tutor.objects.get(tutor=self.request.user)
            tut.wallet += form.instance.amount
            tut.save()
        return super(GetMoney, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GetMoney, self).get_context_data(**kwargs)
        if (Student.objects.filter(student=self.request.user).exists()):
            context['logged_user'] = Student.objects.get(student=self.request.user)
        elif (Tutor.objects.filter(tutor=self.request.user).exists()):
            context['logged_user'] = Tutor.objects.get(tutor=self.request.user)
        return context
