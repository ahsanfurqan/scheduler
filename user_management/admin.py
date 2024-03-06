from django.contrib import admin
from .models import Patient,CustomUser,Counsellor

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_display = ['id', 'username', 'email', 'is_counsellor', 'is_patient']

admin.site.register(CustomUser, CustomUserAdmin)

class PatientAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_display = ['id', 'get_name', 'get_email', 'is_active']
    list_filter = ('is_active', )

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Patient, PatientAdmin)

class CounsellorAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_display = ['id', 'get_name', 'get_email', 'is_active']
    list_filter = ('is_active', )

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Counsellor, CounsellorAdmin)