from rest_framework.serializers import ModelSerializer
from .models import Student,Attendance,Class_attendance,Class_details,Teacher


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
       
class Class_attendanceSerializer(ModelSerializer):
    class Meta:
        model =  Class_attendance
        fields = '__all__'

class Class_detailsSerializer(ModelSerializer):
    class Meta:
        model =  Class_details
        fields = '__all__'

class TeacherSerializer(ModelSerializer):
    class Meta:
        model =  Teacher
        fields = '__all__'