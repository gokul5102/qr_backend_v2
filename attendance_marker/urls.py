from django.contrib import admin
from django.urls import path
from .views import createQR,updateAttendanceRecord,updateLocation,studentLogin,printer

urlpatterns = [
    path('',printer,name='print'),
    path('login/',studentLogin,name='student-login'),
    path('create_qrcode/',createQR,name='create-qrcode'),
    path('update_attendance/<str:id>/',updateAttendanceRecord,name='update-attendance-record'),
    path('update_location/<int:id>/',updateLocation,name='update-location'),
]
