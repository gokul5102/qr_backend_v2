from django.db import models

# Create your models here.
class Student(models.Model):
    UID= models.IntegerField(default=0,unique=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=200,null=True,blank=True)
    class_name=models.IntegerField(default=0)
    class_location_x=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
    class_location_y=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='attendance_of_student')
    encoded_string=models.TextField(null=True)
    # class_location_x=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
    # class_location_y=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
    subject=models.TextField(null=True)
    time_of_lecture=models.TextField(null=True)

    def __str__(self):
        return self.encoded_string


class Class_attendance(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='class_record')
     Physics=models.IntegerField(default=0)
     Chemistry=models.IntegerField(default=0)
     Maths=models.IntegerField(default=0)

     def __str__(self):
        return str(self.student.name)

class Class_details(models.Model):
     room_no=models.IntegerField(default=0)
     lat_1=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
     lat_2=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
     long_1=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
     long_2=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
     altitude=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)

     def __str__(self):
        return str(self.room_no)

class Teacher(models.Model):
    # UID= models.IntegerField(default=0,unique=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=200,null=True,blank=True)
    # class_location_x=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)
    # class_location_y=models.DecimalField(default=0.0, max_digits=500, decimal_places=200)

    def __str__(self):
        return self.name

