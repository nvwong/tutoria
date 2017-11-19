from django.shortcuts import render
from django.views import generic
from tutorial.models import Session, Review
from tutors.models import Tutor
from .models import Student
from datetime import date, time, datetime
# Create your views here.
class MyBookingsList(generic.ListView):
    context_object_name = 'sessions_list'
    template_name = 'mySessions.html'

    def get_queryset(self):
        return Session.objects.filter(student__student=self.request.user)

class ReviewList(generic.ListView):
    model = Session
    template_name = 'review_list.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        student = self.request.user
        username = student.username
        session = Session.objects.filter(student__student__username=username)
        need_review = session.filter(isLocked=True).filter(reviewed=False)
        return need_review


class ReviewForm(generic.DetailView):
    model = Session
    template_name = 'review_form.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewForm, self).get_context_data(**kwargs)
        #If you dont call 'super', you wont have the context processor varibles
        #  like 'user'
        context['user'] = self.request.user # you can add template variables!
        session_id = self.kwargs['pk']
        context['session_id'] = session_id
        return context

def saveReview(request, pk):
    try:
        rating = request.POST['rating']
        content = request.POST['review']
        session = Session.objects.get(id=pk)
    except (KeyError, Session.DoesNotExist):
            # Redisplay the session voting form.
            return render(request, 'review_form.html', {'error_message': "You didn't select a session.",})
    else:
        session.reviewed=True
        rate_time = session.tutor.rate_time
        real_rating = session.review.rating
        real_rating = (real_rating*rate_time + int(rating))/(rate_time+1)
        rate_time+=1
        session.review.time_review = datetime.now()
        session.save()
        return render(request,'review_ok.html')
        #HttpResponseRedirect(reverse('students:reviewok', args=()))
