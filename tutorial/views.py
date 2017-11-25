from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core import mail
from django.urls import reverse
#from django.core.mail import EmailMessage
from .models import Session
from tutors.models import Tutor
from students.models import Student

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
        student.student.wallet +=  amount
        #myTutors.wallet -= amount #transfer money from myTutor to student
        student.save()
        endtime = str(selected_session.end_time)
        body ='Dear ' + selected_session.tutor.tutor.get_full_name() + ',\n' + 'A session booked by ' + student.student.username + ' from ' + str(selected_session.start_time) + ' to ' + str(selected_session.end_time) + ' is cancelled. Go to Tutoria Homapage to check it out.\nTutoria'
        mail.send_mail('A session is cancelled', body, 'admin@tutoria.com', [selected_session.tutor.tutor.email])

        body ='Dear ' + selected_session.student.student.get_full_name() + ',\n' + 'A session taught by '+ selected_session.tutor.tutor.get_full_name() +' from ' + str(selected_session.start_time) + ' to ' + str(selected_session.end_time) + ' is cancelled. Your wallet value now is: $'+ str(student.student.wallet) +'. Go to Tutoria Homapage to check it out.\nTutoria'
        mail.send_mail('A session is cancelled', body, 'admin@tutoria.com', [selected_session.student.student.email])

        selected_session.delete()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request,'cancelok.html')
        #HttpResponseRedirect(reverse('tutorial:cancel_ok'))
