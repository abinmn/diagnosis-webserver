from django.shortcuts import render
from django.views.generic.list import ListView

from api.models import Profile, Data
from django.contrib.auth.models import User

# Create your views here.
class PatientListView(ListView):
    model = Profile
    template_name = 'doctors_portal/patient_list.html'

class PatientDetailsView(ListView):

    template_name = 'doctors_portal/patient_records.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        context['header'] = user.profile_set.all()[0].name
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        records = user.data_set.order_by('-created_at')
        return records