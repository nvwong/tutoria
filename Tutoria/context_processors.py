from tutors.models import Tutor
from students.models import Student

def base_template_name_context_processor(request):
    base_template_name = 'base.html'

    if request.user.is_authenticated():
        if request.user.is_superuser:
            base_template_name = 'base_tutor.html'
        if Tutor.objects.filter(tutor=request.user):
            base_template_name = 'base_tutor.html'

    return {
        'base_template_name': base_template_name,
    }
