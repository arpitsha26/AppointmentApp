from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone

class Customuser(AbstractUser):
    username=None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number=models.CharField(max_length=15,)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserManager()
    
    def __str__(self):
        return self.email



class Doctor(Customuser):
    specialization = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        

class Patient(Customuser):
    Illness = models.TextField(blank=True, null=True) 

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        

class Admin(Customuser):
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
        

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='appointments', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')