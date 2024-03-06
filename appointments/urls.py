from django.urls import path
from .views import AppointmentListCreateView, AppointmentDetailView,PatientAppointmentsListView,CounsellorAppointmentsListView,ActiveAppointmentsDateRangeListView

app_name = 'appointments'

urlpatterns = [
    path('v1/appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('v1/appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('v1/patient-appointments/<int:patient_id>/', PatientAppointmentsListView.as_view(), name='patient-appointments'),
    path('v1/counsellor-appointments/<int:counsellor_id>/', CounsellorAppointmentsListView.as_view(), name='counsellor-appointments'),
    path('v1/active-appointments-date-range/', ActiveAppointmentsDateRangeListView.as_view(), name='active-appointments-date-range'),
]
