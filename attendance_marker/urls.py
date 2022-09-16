from django.contrib import admin
from django.urls import path
from .views import (createQR,updateAttendanceRecord,updateLocation,studentLogin,
TeacherLogin,printer,student_render_pdf_view,teacher_render_pdf_view,tester)

urlpatterns = [
    path('',printer,name='print'),
    path('login/',studentLogin,name='student-login'),
    path('teacher_login/',TeacherLogin,name='teacher-login'),
    path('create_qrcode/',createQR,name='create-qrcode'),
    path('update_attendance/<str:id>/',updateAttendanceRecord,name='update-attendance-record'),
    path('update_location/<int:id>/',updateLocation,name='update-location'),
    path('student_report/<int:id>',student_render_pdf_view,name='student-pdf-view'),
    path('teacher_report/<int:id>',teacher_render_pdf_view,name='teacher-pdf-view'),
    path('tester/',tester,name='tester'),
]
