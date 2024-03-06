from rest_framework import serializers
from .models import Appointment
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        patient = validated_data['patient']
        counsellor = validated_data['counsellor']

        if patient.user == counsellor.user:
            raise serializers.ValidationError("A user cannot book an appointment with themselves.")
         
        # first check if patient or counsellor is active or inactive
        if not patient.is_active:
            raise serializers.ValidationError('Patient is not active and cannot create appointments.')

        if not counsellor.is_active:
            raise serializers.ValidationError('Counsellor is not active and cannot create appointments.')
        
        # Check if there is an active appointment for the patient or counsellor
        existing_appointment = Appointment.objects.filter(patient=patient, counsellor=counsellor, is_active=True).first()

        if existing_appointment:
            # if the appointment date and time is already passed then we should consider them as inactive
            if existing_appointment.appointment_date < timezone.now():
                existing_appointment.is_active = False
                existing_appointment.save()
            else:
                raise serializers.ValidationError('Patient or Counsellor already has an active appointment.')

        # If no active appointment exists, create a new one
        return super().create(validated_data)
