from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseNotFound
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor, Patient, Appointment
from django.core.paginator import Paginator
from django.urls import reverse_lazy

class ClinicView(ListView):
    model = Appointment
    template_name = 'clinicHome.html'
    context_object_name = 'appointments'
    paginate_by = 2

    def get_queryset(self):
        return Appointment.objects.filter(status='a').order_by('date', 'time')

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
        appointments = self.object.appointment_set.filter(status='a')
        context['appointments'] = appointments
        context['is_patient'] = hasattr(self.request.user, 'patient')
        return context

    def post(self, request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            return HttpResponseForbidden("Only patients can book appointments.")
        
        appointment_id = request.POST.get('appointment')
        if appointment_id:
            appointment = get_object_or_404(Appointment, id=appointment_id, status='a')
            appointment.status = 't'
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('my_appointments')
        return redirect('doctor_detail', pk=kwargs['pk'], slug=kwargs['slug'])

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

class NewAppointmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    template_name = 'new_appointment.html'
    fields = ['date', 'time']
    success_url = reverse_lazy('home')

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.instance.status = 'a'
        return super().form_valid(form)

@login_required
def my_appointments(request):
    if hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor, status='t')
    elif hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient, status='t')
    else:
        return HttpResponseForbidden("You don't have permission to view appointments.")
    
    return render(request, 'my_appointments.html', {'appointments': appointments})
