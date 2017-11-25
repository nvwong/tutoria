from django.contrib import admin
from .models import Tutor, Course, NotAvailableSlot, Tag

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(NotAvailableSlot)
admin.site.register(Tag)
