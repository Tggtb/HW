from django.urls import path
from . import views # the "." means current directory

urlpatterns = [
 path('', views.ClinicView.as_view(), name='home'),
 path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
 path('doctors/<int:pk>-<slug:slug>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
 path('patients/', views.PatientListView.as_view(), name='patient_list'),
 path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
 path('newappoint/', views.NewAppointmentView.as_view(), name='new_appointment'),
 path('myappoint/', views.my_appointments, name='my_appointments'),
 path('available-appointments/', views.AvailableAppointmentListView.as_view(), name='available_appointments_list'),
]