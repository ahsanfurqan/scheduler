from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ['patient__user__username', 'counsellor__user__username', 'appointment_date']
    list_display = ['id', 'get_patient_name', 'get_counsellor_name', 'appointment_date', 'is_active']
    list_filter = ('is_active', 'patient', 'counsellor', 'appointment_date')


    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.short_description = 'Patient Name'

    def get_counsellor_name(self, obj):
        return f"{obj.counsellor.user.first_name} {obj.counsellor.user.last_name}"
    get_counsellor_name.short_description = 'Counsellor Name'

admin.site.register(Appointment, AppointmentAdmin)