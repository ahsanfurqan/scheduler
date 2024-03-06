from django.db import models
from user_management.models import CustomUser

class Appointment(models.Model):
    patient = models.ForeignKey('user_management.Patient', on_delete=models.CASCADE)
    counsellor = models.ForeignKey('user_management.Counsellor', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
