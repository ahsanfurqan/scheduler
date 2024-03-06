from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Patient, Counsellor

class CustomUserSerializersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient("http://127.0.0.1:8000")

    def create_user(self, data):
        return self.client.post(f'/api/v1/register/', data, format='json')

    def test_create_user_with_valid_data(self):
        data = {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'is_counsellor': True,
            'is_patient': False,
            'password': 'StrongPassword123',
        }

        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user, counsellor, and patient were created
        user = CustomUser.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))

        counsellor = Counsellor.objects.get(user=user)
        self.assertTrue(counsellor.is_active)

        # Ensure that no patient was created
        with self.assertRaises(Patient.DoesNotExist):
            Patient.objects.get(user=user)

    def test_create_user_with_invalid_data(self):
        data = {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'is_counsellor': False,
            'is_patient': False,
            'password': 'Weak',
        }

        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class PatientUpdateSerializerTestCase(TestCase):
    def setUp(self):
        # Create a test user, patient, and counsellor for the test
        self.user = CustomUser.objects.create_user(
            username='test_user',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            is_counsellor=True,
            is_patient=True,
            password='StrongPassword123',
        )
        self.patient = Patient.objects.create(user=self.user, is_active=True)
        self.counsellor = Counsellor.objects.create(user=self.user, is_active=True)

        # Create an API client for making requests
        self.client = APIClient("http://127.0.0.1:8000")

    def test_update_patient_with_valid_data(self):
        # Data to update the patient
        data = {
            'user': {
                'first_name': 'UpdatedFirstName',
                'last_name': 'UpdatedLastName',
                'is_counsellor': False,  # Update is_counsellor field
            }
        }

        # Make a PUT request to update the patient
        response = self.client.put(f'/api/v1/patients/{self.patient.id}/', data, format='json')

        # Check if the update was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the patient instance from the database
        self.patient.refresh_from_db()

        # Check if the user fields are updated
        self.assertEqual(self.patient.user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.patient.user.last_name, 'UpdatedLastName')

        # Check if the associated counsellor is deactivated
        self.assertFalse(Counsellor.objects.get(user=self.user).is_active)

    def test_update_patient_with_invalid_data(self):
        # Invalid data that would fail validation
        invalid_data = {
            'user': {
                'is_counsellor': 'InvalidBooleanValue',  # Invalid value for boolean field
            }
        }

        # Make a PUT request with invalid data
        response = self.client.put(f'/api/v1/patients/{self.patient.id}/', invalid_data, format='json')

        # Check if the update fails due to validation errors (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class CounsellorUpdateSerializerTestCase(TestCase):
    def setUp(self):
        # Create a test user, patient, and counsellor for the test
        self.user = CustomUser.objects.create_user(
            username='test_user',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            is_counsellor=True,
            is_patient=True,
            password='StrongPassword123',
        )
        self.counsellor = Counsellor.objects.create(user=self.user, is_active=True)
        self.patient = Patient.objects.create(user=self.user, is_active=True)

        # Create an API client for making requests
        self.client = APIClient("http://127.0.0.1:8000")

    def test_update_counsellor_with_valid_data(self):
        # Data to update the counsellor
        data = {
            'user': {
                'first_name': 'UpdatedFirstName',
                'last_name': 'UpdatedLastName',
                'is_patient': False,  # Update is_patient field
            }
        }

        # Make a PUT request to update the counsellor
        response = self.client.put(f'/api/v1/counsellors/{self.counsellor.id}/', data, format='json')

        # Check if the update was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the counsellor instance from the database
        self.counsellor.refresh_from_db()

        # Check if the user fields are updated
        self.assertEqual(self.counsellor.user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.counsellor.user.last_name, 'UpdatedLastName')

        # Check if the associated patient is deactivated
        self.assertFalse(Patient.objects.get(user=self.user).is_active)

    def test_update_counsellor_with_invalid_data(self):
        # Invalid data that would fail validation
        invalid_data = {
            'user': {
                'is_patient': 'InvalidBooleanValue',  # Invalid value for boolean field
            }
        }

        # Make a PUT request with invalid data
        response = self.client.put(f'/api/v1/counsellors/{self.counsellor.id}/', invalid_data, format='json')

        # Check if the update fails due to validation errors (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)