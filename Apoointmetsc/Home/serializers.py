from rest_framework import serializers
from .models import Customuser, Doctor, Patient, Admin, Appointment

class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number','password']

class DoctorSerializer(CustomuserSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'specialization','password']

class PatientSerializer(CustomuserSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'Illness','password']

class AdminSerializer(CustomuserSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number','password']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'status']