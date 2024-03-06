from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.filters import OrderingFilter
from django.utils import timezone

class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.filter(is_active=True)
    serializer_class = AppointmentSerializer

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.filter(is_active=True)
    serializer_class = AppointmentSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class PatientAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Appointment.objects.filter(patient__id=patient_id, is_active=True)

class CounsellorAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        return Appointment.objects.filter(counsellor__id=counsellor_id, is_active=True)


class ActiveAppointmentsDateRangeListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-appointment_date']

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Assuming both date needs to be present
        if not start_date or not end_date:
            return Appointment.objects.none()

        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()

        return Appointment.objects.filter(
            is_active=True,
            appointment_date__range=(start_date, end_date)
        )