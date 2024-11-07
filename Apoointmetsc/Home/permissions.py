from rest_framework import permissions

class IsAdminOrSuperUser(permissions.BasePermission): #allow only admin and superuser to create doctor
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsSuperUserOnly(permissions.BasePermission):  #allow ony superuser to create admin

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
     
class IsPatient(permissions.BasePermission):     #check user is patient or not 
    def has_permission(self, request, view):
        return hasattr(request.user, 'patient')

class IsDoctor(permissions.BasePermission): #check user is Doctor or not
    def has_permission(self, request, view):
        return hasattr(request.user, 'doctor')
