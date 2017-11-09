from django.db import models

# Create your models here.

class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    isLocked = models.BooleanField(default=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    tutor = models.ForeignKey('tutors.Tutor', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.isLocked)
