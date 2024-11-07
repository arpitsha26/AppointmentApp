from django.contrib import admin
from django.urls import include, path
from .views import Signup, Patientsignup, Doctorsignup, Adminsignup

urlpatterns = [
    path('signup/', Signup.as_view(), name='sign_up'),
    path('signup/patient/',Patientsignup.as_view(), name='patient_signup'),
    path('signup/doctor/', Doctorsignup.as_view(), name='doctor_signup'),
    path('signup/admin/', Adminsignup.as_view(), name='admin_signup'),
    
]
