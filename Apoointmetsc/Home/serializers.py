from rest_framework import serializers
from .models import Customuser, Doctor, Patient, Admin, Appointment
from django.contrib.auth.hashers import make_password

class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number','password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = Customuser(
        email=validated_data['email'],
        first_name=validated_data.get('first_name'),
        last_name=validated_data.get('last_name'),
        phone_number=validated_data.get('phone_number'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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