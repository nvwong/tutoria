from django.db import models
from django.contrib.auth.models import User
from django_cron import CronJobBase, Schedule
from tutors.models import Tutor
from students.models import Student
from datetime import date, time, datetime, timedelta
from decimal import Decimal

# Create your models here.
# Documentation of cron job: https://pypi.python.org/pypi/django-cron/0.2.8 http://django-cron.readthedocs.io/en/latest/installation.html
class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    isLocked = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.start_time)

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
        current_time = timezone.now()
        for session in session_list:
            if session.start_time == current_time:
                session.isLocked = True
            if session.end_time == current_time:
                tw = Wallet.objects.get(owner=session.tutor.tutor)
                tw.balance += Decimal(session.tutor.hourlyRate)
                tw.save()
                adminac = User.objects.get(username="admin")
                aw = Wallet.objects.get(owner=adminac)
                aw.balance += Decimal(session.tutor.hourlyRate * 0.05)
                aw.save()
            session.save()
                #myTutors.wallet += session.tutor.hourly_rate*0.05
