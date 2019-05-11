from django.urls import path
from doctors_portal.views import *

urlpatterns = [
    path('patient-list', PatientListView.as_view(), name="patient-list"),
    path('patient-list/<int:pk>', PatientDetailsView.as_view(), name='patient-list')
]