from django.contrib import admin
from .models import Student,Attendance,Class_attendance,Class_details

# Register your models here.
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Class_attendance)
admin.site.register(Class_details)
