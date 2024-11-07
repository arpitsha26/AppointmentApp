from django.contrib import admin
from .models import Customuser,Doctor,Admin,Appointment,Patient

admin.site.register(Customuser)
admin.site.register(Doctor)
admin.site.register(Admin)
admin.site.register(Patient)
admin.site.register(Appointment)

