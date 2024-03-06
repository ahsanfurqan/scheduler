from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Appointment
from user_management.models import Patient,Counsellor,CustomUser
from datetime import datetime, timedelta

class AppointmentSerializerTestCase(TestCase):
    def setUp(self):
        # Create test patient and counsellor
        self.patient_user = CustomUser.objects.create_user(
            username='patient_user',
            first_name='Patient',
            last_name='User',
            email='patient@example.com',
            is_patient=True,
            is_counsellor=False,
            password='StrongPassword123',
        )
        self.counsellor_user = CustomUser.objects.create_user(
            username='counsellor_user',
            first_name='Counsellor',
            last_name='User',
            email='counsellor@example.com',
            is_patient=False,
            is_counsellor=True,
            password='StrongPassword456',
        )
        self.user = CustomUser.objects.create_user(
            username='custom_user',
            first_name='Counsellor',
            last_name='Patient',
            email='counsellor.patient@example.com',
            is_patient=True,
            is_counsellor=True,
            password='StrongPassword456',
        )
        Patient.objects.create(user=self.user)
        Counsellor.objects.create(user=self.user)

        self.patient = Patient.objects.create(user=self.patient_user, is_active=True)
        self.counsellor = Counsellor.objects.create(user=self.counsellor_user, is_active=True)

        # Create an API client for making requests
        self.client = APIClient("http://127.0.0.1:8000")

    def test_create_appointment_with_valid_data(self):
        # Data to create a new appointment
        appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=1)).isoformat(),  # Set the appointment for tomorrow
            'is_active': True,
        }

        # Make a POST request to create the appointment
        response = self.client.post('/api/v1/appointments/', appointment_data, format='json')

        # Check if the appointment creation was successful (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the appointment was created in the database
        appointment = Appointment.objects.get(patient=self.patient, counsellor=self.counsellor)
        self.assertTrue(appointment.is_active)

    def test_create_appointment_with_inactive_patient(self):
        # Set the patient to inactive
        self.patient.is_active = False
        self.patient.save()

        # Data to create a new appointment with an inactive patient
        appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the appointment
        response = self.client.post('/api/v1/appointments/', appointment_data, format='json')

        # Check if the appointment creation fails due to an inactive patient (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_with_inactive_counsellor(self):
        # Set the counsellor to inactive
        self.counsellor.is_active = False
        self.counsellor.save()

        # Data to create a new appointment with an inactive counsellor
        appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the appointment
        response = self.client.post('/api/v1/appointments/', appointment_data, format='json')

        # Check if the appointment creation fails due to an inactive counsellor (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_with_existing_active_appointment(self):
        # Create an existing active appointment for the patient and counsellor
        existing_appointment = Appointment.objects.create(
            patient=self.patient,
            counsellor=self.counsellor,
            appointment_date=(datetime.now() + timedelta(days=2)),
            is_active=True,
        )

        # Data to create a new appointment with the same patient and counsellor
        new_appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=3)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the new appointment
        response = self.client.post('/api/v1/appointments/', new_appointment_data, format='json')

        # Check if the appointment creation fails due to an existing active appointment (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_with_existing_inactive_appointment(self):
        # Create an existing inactive appointment for the patient and counsellor
        existing_appointment = Appointment.objects.create(
            patient=self.patient,
            counsellor=self.counsellor,
            appointment_date=(datetime.now() + timedelta(days=2)),
            is_active=False,
        )

        # Data to create a new appointment with the same patient and counsellor
        new_appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=3)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the new appointment
        response = self.client.post('/api/v1/appointments/', new_appointment_data, format='json')

        # Check if the appointment creation is successful (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_appointment_with_existing_active_appointment_and_past_date(self):
        # Create an existing active appointment for the patient and counsellor with a past date
        existing_appointment = Appointment.objects.create(
            patient=self.patient,
            counsellor=self.counsellor,
            appointment_date=(datetime.now() - timedelta(days=1)),
            is_active=True,
        )

        # Data to create a new appointment with the same patient and counsellor
        new_appointment_data = {
            'patient': self.patient.id,
            'counsellor': self.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the new appointment
        response = self.client.post('/api/v1/appointments/', new_appointment_data, format='json')

        # Check if the appointment creation is successful (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the existing appointment is deactivated due to a past date
        existing_appointment.refresh_from_db()
        self.assertFalse(existing_appointment.is_active)

    def test_create_appointment_with_same_patient_and_counsellor(self):
        # Data to create a new appointment with the same patient and counsellor
        appointment_data = {
            'patient': self.user.patient.id,
            'counsellor': self.user.counsellor.id,
            'appointment_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'is_active': True,
        }

        # Make a POST request to create the appointment
        response = self.client.post('/api/v1/appointments/', appointment_data, format='json')

        # Check if the appointment creation fails due to the same patient and counsellor (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
