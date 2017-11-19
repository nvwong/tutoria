from django.db import models
from django_cron import CronJobBase, Schedule
from tutors.models import Tutor
from students.models import Student
from datetime import date, time, datetime, timedelta
# Create your models here.
# Documentation of cron job: https://pypi.python.org/pypi/django-cron/0.2.8 http://django-cron.readthedocs.io/en/latest/installation.html
class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    isLocked = models.BooleanField(default=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    tutor = models.ForeignKey('tutors.Tutor', on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.isLocked)

class Review(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    content = models.CharField(blank=True, max_length=100)
    time_review = models.DateTimeField(null=True, blank=True)
    rating = models.FloatField(blank=True, default=0)
    def __str__(self):
        return str(self.time_review)

class Lock_and_End(CronJobBase):
    RUN_EVERY_30MINS = 30 # every 30 minutes
    RUN_AT_TIMES = ['9:00']
    schedule = Schedule(run_every_mins=RUN_EVERY_30MINS, run_at_times=RUN_AT_TIMES)
    code = 'tutorial.lock_and_end'    # a unique code
    #ALLOW_PARALLEL_RUNS = True

    def do(self):
        # do your thing here
        session_list = Session.objects.all()
        current_time = time.now()
        for session in session_list:
            if session.start_time == current_time:
                session.isLocked = True
            if session.end_time == current_time:
                session.tutor.tutor.wallet += session.tutor.hourly_rate
            session.save()
                #myTutors.wallet += session.tutor.hourly_rate*0.05
