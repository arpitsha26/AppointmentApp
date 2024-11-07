from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrSuperUser, IsSuperUserOnly
from .serializers import PatientSerializer, DoctorSerializer, AdminSerializer
from django.contrib.auth import get_user_model

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
    permission_classes = [IsAdminOrSuperUser] 
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Adminsignup(APIView):
    permission_classes = [IsSuperUserOnly] 

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

