from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsAdminOrSuperUser, IsSuperUserOnly, IsPatient
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
