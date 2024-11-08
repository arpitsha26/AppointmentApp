from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsAdminOrSuperUser, IsSuperUserOnly, IsPatient, IsDoctor
from .serializers import PatientSerializer, DoctorSerializer, AdminSerializer, AppointmentSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Doctor, Patient, Admin, Appointment

User = get_user_model()

class Signup(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        signup_links = {
            "patient_signup": request.build_absolute_uri('/signup/patient/'),
            "doctor_signup": request.build_absolute_uri('/signup/doctor/'),
            "admin_signup": request.build_absolute_uri('/signup/admin/')
        }
        return Response(signup_links)
    
class Patientsignup(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Doctorsignup(APIView):
    permission_classes = [IsAdminOrSuperUser,IsAuthenticated] 
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Adminsignup(APIView):
    permission_classes = [IsAuthenticated,IsSuperUserOnly] 

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Createappointment(APIView):
    permission_classes=[IsAuthenticated,IsPatient]
    def post(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response({'error': 'Doctor ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
        serializer = AppointmentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            appointment = serializer.save(doctor=doctor)
            return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Showappointments(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email-required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        appointments = Appointment.objects.filter(patient=patient, status='scheduled') 
        serializer = AppointmentSerializer(appointments, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK) 

class Getdoctor(APIView):
    permission_classes = [IsAuthenticated, IsPatient]  

    def get(self, request):
        specialization = request.query_params.get('specialization')
        if not specialization:
            return Response({'error': 'Specialization-required'}, status=status.HTTP_400_BAD_REQUEST)
        doctors = Doctor.objects.filter(specialization=specialization)
        if not doctors:
            return Response({'error': 'No doctors found '}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Markcomplete(APIView):
    permission_classes = [IsDoctor] 
    
    def patch(self, request):
        appointment_id = request.query_params.get('appointment_id')
        
        if not appointment_id:
            return Response({'error': 'Appointmentid- required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if appointment.doctor != request.user.doctor:
            return Response({'error': 'you are not appointed doctor to this appointment'}, status=status.HTTP_403_FORBIDDEN)

        appointment.status = 'completed'
        appointment.save()
        return Response({
            'messg': 'mark completed done',
            'appointment': {
                'id': appointment.id,
                'status': appointment.status
            }
        }, status=status.HTTP_200_OK)
