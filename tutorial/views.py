from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core import mail
from django.urls import reverse
#from django.core.mail import EmailMessage
from .models import Session
from tutors.models import Tutor, NotAvailableSlot
from students.models import Student
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone
import datetime

# Create your views here.
class ShowOneSession(generic.DetailView):
    model = Session
    template_name = 'oneSession.html'

class sessionListView(generic.ListView):
    model = Session
    template_name = 'session_list.html'
    context_object_name = 'latest_session_list'

    def get_queryset(self):
        student = self.request.user
        username = student.username
        return Session.objects.filter(student__student__username=username).filter(isLocked=False)

    def get_context_data(self, **kwargs):
        context = super(sessionListView, self).get_context_data(**kwargs)
        #If you dont call 'super', you wont have the context processor varibles
        #  like 'user'
        context['user'] = self.request.user # you can add template variables!
        return context

class MakeBooking (SuccessMessageMixin, generic.CreateView):
    model = Session
    fields = ['start_time']
    template_name = "bookSession.html"
    success_url = reverse_lazy('students:mybookings')
    success_message = 'Booking Successful.'

    def form_valid(self, form):
        ok = True

        the_student = Student.objects.get(student=self.request.user)
        the_tutor = Tutor.objects.get(pk=self.kwargs['tutor_id'])
        notAvailable = NotAvailableSlot.objects.filter(tutor=the_tutor)
        st = form.instance.start_time
        et = st + datetime.timedelta(minutes=the_tutor.timePerSlot)

        for slot in notAvailable:
            if (slot.start_time <= st) and (slot.end_time >= et):
                ok = False
                messages.error(self.request, 'Crashed with Tutor Unavailable Slots.')

        if ok:
            mylist = Session.objects.filter(student=the_student)
            for booking in mylist:
                if (booking.start_time.date() == st.date()) and (booking.tutor == the_tutor):
                    ok = False
                    messages.error(self.request, 'Cannot book more than one slot of same tutor in a day.')

            if (st - timezone.now() <= datetime.timedelta(hours=24)):
                ok = False
                messages.error(self.request, 'Cannot book session within coming 24 hours.')

            if (st - timezone.now() > datetime.timedelta(days=7)):
                ok = False
                messages.error(self.request, 'Cannot book further than 7 days.')

            if (the_student.wallet < (the_tutor.hourlyRate)*1.05):
                ok = False
                messages.error(self.request, 'You do not have enough money.')

        if ok:
            form.instance.student = the_student
            form.instance.tutor = the_tutor
            form.instance.end_time = et
            new_unavail = NotAvailableSlot(tutor=the_tutor, start_time=st, end_time=et)
            new_unavail.save()
            the_student.wallet -= (the_tutor.hourlyRate)*1.05
            the_student.save()

            body ='Dear ' + the_tutor.tutor.get_full_name() + ',\n' + 'A session is booked by ' + the_student.student.get_full_name() + ' from ' + str(st) + ' to ' + str(et) + '. Go to Tutoria Homapage to check it out.\nTutoria'
            mail.send_mail('A session is booked', body, 'admin@tutoria.com', [the_tutor.tutor.email])

            body ='Dear ' + the_student.student.get_full_name() + ',\n' + 'A session taught by '+ the_tutor.tutor.get_full_name() +' from ' + str(st) + ' to ' + str(et) + ' is booked. Your wallet value now is: $'+ str(the_student.wallet) +'. Go to Tutoria Homepage to check it out.\nTutoria'
            mail.send_mail('A session is cancelled', body, 'admin@tutoria.com', [the_student.student.email])

            return super(MakeBooking, self).form_valid(form)
        else:
            return super(MakeBooking, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MakeBooking, self).get_context_data(**kwargs)
        #If you dont call 'super', you wont have the context processor varibles
        #  like 'user'
        tut = Tutor.objects.get(pk=self.kwargs['tutor_id'])
        context['tutor'] = tut
        context['fee'] = tut.hourlyRate*1.05
        context['unavailability_list'] = NotAvailableSlot.objects.all()
        return context



class CancelokView(generic.DetailView):
    model = Session
    template_name = 'cancelok.html'

def cancel(request):
    try:
        selected_session = Session.objects.get(pk=request.POST['choice'])
    except (KeyError, Session.DoesNotExist):
        # Redisplay the session voting form.
        return render(request, 'session_list.html', {'error_message': "You didn't select a session.",})
    else:
        student = request.user
        amount = selected_session.tutor.hourlyRate * 1.05
        student.student.wallet += amount
        #myTutors.wallet -= amount #transfer money from myTutor to student
        student.save()
        endtime = str(selected_session.end_time)
        body ='Dear ' + selected_session.tutor.tutor.get_full_name() + ',\n' + 'A session booked by ' + student.username + ' from ' + str(selected_session.start_time) + ' to ' + str(selected_session.end_time) + ' is cancelled. Go to Tutoria Homapage to check it out.\nTutoria'
        mail.send_mail('A session is cancelled', body, 'admin@tutoria.com', [selected_session.tutor.tutor.email])

        body ='Dear ' + selected_session.student.student.get_full_name() + ',\n' + 'A session taught by '+ selected_session.tutor.tutor.get_full_name() +' from ' + str(selected_session.start_time) + ' to ' + str(selected_session.end_time) + ' is cancelled. Your wallet value now is: $'+ str(student.student.wallet) +'. Go to Tutoria Homapage to check it out.\nTutoria'
        mail.send_mail('A session is cancelled', body, 'admin@tutoria.com', [selected_session.student.student.email])

        unavail = NotAvailableSlot.objects.get(tutor=selected_session.tutor, start_time=selected_session.start_time, end_time=selected_session.end_time)
        unavail.delete()
        selected_session.delete()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request,'cancelok.html')
        #HttpResponseRedirect(reverse('tutorial:cancel_ok'))
