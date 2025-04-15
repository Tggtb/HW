from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseNotFound
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView
from .models import Doctor, Patient, Appointment

class ClinicView(TemplateView):
    template_name = 'clinicHome.html'

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return Doctor.objects.order_by('user__last_name', 'user__first_name')

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = self.object.appointment_set.all()
        return context

class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return Patient.objects.order_by('user__last_name', 'user__first_name')

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def get_object(self, queryset=None):
        return get_object_or_404(Patient, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = self.object.appointment_set.filter(status='t')
        context['appointments'] = appointments if appointments.exists() else None
        return context

class AvailableAppointmentListView(ListView):
    model = Appointment
    template_name = 'available_appointments_list.html'
    context_object_name = 'appointments'
    queryset = Appointment.objects.filter(status='a')
