from django.contrib import admin
from django.urls import include, path
from .views import Signup, Patientsignup, Doctorsignup, Adminsignup, Createappointment, Showappointments, Getdoctor
from rest_framework_simplejwt.views import  TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('signup/', Signup.as_view(), name='sign_up'),
    path('signup/patient/',Patientsignup.as_view(), name='patient_signup'),
    path('signup/doctor/', Doctorsignup.as_view(), name='doctor_signup'),
    path('signup/admin/', Adminsignup.as_view(), name='admin_signup'),
    path('login/',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createAppointment/', Createappointment.as_view(), name='create_appointment'),
    path('showAppointment/', Showappointments.as_view(), name='show_appointment'),
    path('getdoctor/',Getdoctor.as_view(), name='get_doctor'),
    
    
]