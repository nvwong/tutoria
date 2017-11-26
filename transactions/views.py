from django.shortcuts import render
from django.views import generic
from .models import Transaction, Wallet
from students.models import Student
from tutors.models import Tutor
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
class AddMoney (SuccessMessageMixin, generic.CreateView):
    model = Transaction
    fields = ['amount']
    template_name = "addmoney.html"
    success_message = 'Adding Money Successful.'
    success_url = reverse_lazy('transaction:add')

    def form_valid(self, form):
        wallet = Wallet.objects.get(owner=self.request.user)
        form.instance.owner = self.request.user
        form.instance.timestamp = timezone.now()
        wallet.balance += form.instance.amount
        wallet.save()
        self.object = form.save()
        return super(AddMoney, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddMoney, self).get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(owner=self.request.user)
        return context

class GetMoney (SuccessMessageMixin, generic.CreateView):
    model = Transaction
    fields = ['amount']
    template_name = "getmoney.html"
    success_message = 'Getting Money Successful.'
    success_url = reverse_lazy('transaction:get')

    def form_valid(self, form):
        wallet = Wallet.objects.get(owner=self.request.user)

        ok = True
        if (wallet.balance < form.instance.amount):
            ok = False
            messages.error(self.request, 'Not enough money.')

        if ok:
            form.instance.owner = self.request.user
            form.instance.timestamp = timezone.now()
            form.instance.amount = -(form.instance.amount)
            self.object = form.save()
            wallet.balance += form.instance.amount
            wallet.save()
            return super(GetMoney, self).form_valid(form)
        else:
            return super(GetMoney, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(GetMoney, self).get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(owner=self.request.user)
        return context
