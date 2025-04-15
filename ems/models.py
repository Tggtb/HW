from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def get_absolute_url(self):
        return reverse('doctor_detail', args=[self.id, self.slug])

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"

class Appointment(models.Model):
    appointID = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.CharField(max_length=5)
    STATUS = (('a', 'Available'), ('t', 'Taken'), ('d', 'Done'))
    status = models.CharField(max_length=1, choices=STATUS, default='a')

    def __str__(self):
        return f"Appointment {self.appointID} - {self.date} {self.time}"