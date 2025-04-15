from django.contrib import admin
from .models import Doctor, Patient, Appointment

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user_last_name', 'user_first_name')

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user_last_name', 'user_first_name')

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status')
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Appointment,AppointmentAdmin)