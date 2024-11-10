from rest_framework import serializers
from .models import Customuser, Doctor, Patient, Admin, Appointment
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

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
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = Customuser.objects.get(email=email)
            if not hasattr(user, 'patient'):  
                raise serializers.ValidationError("User is not a patient.")
        except Customuser.DoesNotExist:
            raise serializers.ValidationError("No user .")
        
        self.context['user'] = user
        return email

    def save(self):

        user = self.context['user']
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"http://127.0.0.1:8000/password/reset/confirm/{token}/?user_id={user.id}"
        
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )