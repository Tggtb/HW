from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)

# Create ClinicStaff group if it doesn't exist
clinic_staff_group, created = Group.objects.get_or_create(name='ClinicStaff')

# Get the content type for Appointment model
appointment_content_type = ContentType.objects.get_for_model(Appointment)

# Get the "add_appointment" permission
add_appointment_permission = Permission.objects.get(
    codename='add_appointment',
    content_type=appointment_content_type
)

# Add the permission to the group if it's not already there
if add_appointment_permission not in clinic_staff_group.permissions.all():
    clinic_staff_group.permissions.add(add_appointment_permission)