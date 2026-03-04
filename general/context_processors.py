from .models import *
from personnel.models import *
from django.db.models import Q

def count_action_list(request):
    if request.user.is_authenticated:
        count = Report.objects.filter(is_submitted=True, is_approved=False, office=request.user.users_profile.office).count()
        return {'count_action_list': count}
    return {}