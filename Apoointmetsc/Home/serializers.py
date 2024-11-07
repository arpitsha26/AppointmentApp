from rest_framework import serializers
from .models import Customuser, Doctor, Patient, Admin, Appointment
from django.contrib.auth.hashers import make_password

class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

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
        
    
    def create(self, validated_data):
        patient = self.context['request'].user.patient # get the patient from the request context
        appointment = Appointment.objects.create(  # Associate the patient with the appointment
            patient=patient,
            doctor=validated_data['doctor'],
            appointment_date=validated_data['appointment_date'],
            status=validated_data['status']
        )
        return appointment