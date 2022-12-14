from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student,Attendance,Class_attendance,Class_details,Teacher
from .serializers import StudentSerializer,AttendanceSerializer,TeacherSerializer
from .utils import  generate_QR,generate_key,StudentIsPresent
from rest_framework import status
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
import os
import json
from pathlib import Path
from django.http import HttpResponse,JsonResponse
import threading
import time
from .tasks import send_mail_func

from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(["GET"])
def printer(request):
    print(request.META['SERVER_PORT'])
    return Response("Done", status=status.HTTP_200_OK)

@api_view(["GET"])
def tester(request):
    stu=Student.objects.all()
    ser = StudentSerializer(stu)
    return JsonResponse(ser.data,status= status.HTTP_200_OK)

#teacher genrates QR code 
@api_view(["POST"])
def createQR(request):
    stu=Student.objects.all()
    if request.data:
        subject = request.data.get('subject')
        time = request.data.get('time')
        room_no=request.data.get('room_no')
        # try:
        #     c=Class_details.objects.get(room_no=room_no)
        # except Class_details.DoesNotExist:
        #     c = None
        # print(c,stu)
        send_mail_func.delay(subject,time,room_no)
        # for i in stu:
        #     uid = i.UID
        #     stu_x=i.class_location_x
        #     stu_y=i.class_location_y
        #     print(uid,' ',StudentIsPresent(stu_x,stu_y,c.lat_1,c.lat_2,c.long_1,c.long_2))
        #     if StudentIsPresent(stu_x,stu_y,c.lat_1,c.lat_2,c.long_1,c.long_2):
        #         enc_key=generate_key(uid,i.name,subject,time,c.lat_1,c.long_1)
        #         a=Attendance.objects.create(student=i,encoded_string=enc_key,subject=subject,time_of_lecture=time)
        #         a.save()
        #         generate_QR(enc_key)
        #         s, from_email, to = "Your attendance for today\'s lecture", 'gokul.ramanan@spit.ac.in', i.email
        #         text_content = 'This is an important message.'
        #         html_content = '<p>This is an <strong>important</strong> message.</p>'
        #         msg = EmailMultiAlternatives(s, text_content, from_email, [to])
        #         msg.attach_alternative(html_content, "text/html")
        #         image=f"{enc_key}.png"
        #         file_path = os.path.join(BASE_DIR,image)
        #         with open(file_path, 'rb') as f:
        #             img = MIMEImage(f.read())
        #             img.add_header('Content-ID', '<{name}>'.format(name=image))
        #             img.add_header('Content-Disposition', 'inline', filename=image)
        #         msg.attach(img)
        #         msg.send()
        return Response("Done", status=status.HTTP_201_CREATED)
    return Response("error", status=status.HTTP_400_BAD_REQUEST)

#part2
@api_view(["POST"])
def updateAttendanceRecord(request,id):
    u=Attendance.objects.get(encoded_string=id)#id passed in url from frontend
    # print("u",u,type(u))
    if(u):
        stu=u.student
        print("stu",stu)
        subject = u.subject
        subject=subject.lower()
        if(subject=="physics"):
            c=Class_attendance.objects.get(student=stu)
            c.Physics+=1
            c.save()
            path=os.path.join(BASE_DIR,f"{u.encoded_string}.png")
            os.remove(path)
            u.delete()
        elif(subject=="chemistry"):
            c=Class_attendance.objects.get(student=stu)
            c.Chemistry+=1
            c.save()
            path=os.path.join(BASE_DIR,f"{u.encoded_string}.png")
            os.remove(path)
            u.delete()
        elif(subject=="maths"):
            c=Class_attendance.objects.get(student=stu)
            c.Maths+=1
            c.save()
            path=os.path.join(BASE_DIR,f"{u.encoded_string}.png")
            os.remove(path)
            u.delete()
        else:
            path=os.path.join(BASE_DIR,f"{u.encoded_string}.png")
            os.remove(path)
            u.delete()
            return Response("Wrong subject!", status=status.HTTP_400_BAD_REQUEST)
        return Response("Updated status", status=status.HTTP_201_CREATED)
    return Response("error", status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def updateLocation(request,id):
    print("11",request.data)
    if request.data:
        class_location_x = request.data.get('class_location_x')
        class_location_y = request.data.get('class_location_y')
        stu=Student.objects.get(UID=id)
        stu.class_location_x=class_location_x
        stu.class_location_y=class_location_y
        stu.save()
        t = threading.Thread(target=ResetLocation,args=(id,))
        t.start()
        return Response("Updated location", status=status.HTTP_201_CREATED)
    return Response("error", status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def studentLogin(request):
    print("12",request.data)
    if request.data:
        email = request.data.get('email')
        password = request.data.get('password')
        stu=Student.objects.get(email=email,password=password)
        if(stu):
            ser = StudentSerializer(stu)
            return JsonResponse(ser.data,status= status.HTTP_200_OK)
        else :
            return Response("No student found", status=status.HTTP_400_BAD_REQUEST)
    return Response("error", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def TeacherLogin(request):
    print("12",request.data)
    if request.data:
        email = request.data.get('email')
        password = request.data.get('password')
        t=Teacher.objects.get(email=email,password=password)
        if(t):
            ser = TeacherSerializer(t)
            return JsonResponse(ser.data,status= status.HTTP_200_OK)
        else :
            return Response("No teacher found", status=status.HTTP_400_BAD_REQUEST)
    return Response("error", status=status.HTTP_400_BAD_REQUEST)


#report for every student
def student_render_pdf_view(request,*args,**kwargs):
    id=kwargs.get('id')
    student=get_object_or_404(Student,UID=id)
    c=Class_attendance.objects.get(student=student)
    template_path = 'attendance_marker/pdf2.html'
    context = {'student': student,'c':c}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#report for teacher
def teacher_render_pdf_view(request,*args,**kwargs):
    l=[]
    Class=kwargs.get('id')
    students=Student.objects.filter(class_name=Class).order_by('UID')
    c=Class_attendance.objects.filter(student__class_name=Class).order_by('student__UID')
    print(c)
    for i in range (len(students)):
        dict = {}
        dict['name']=students[i].name
        dict['email']=students[i].email
        dict['UID']=students[i].UID
        dict['Physics']=c[i].Physics
        dict['Chemistry']=c[i].Chemistry
        dict['Maths']=c[i].Maths
        l.append(dict)
    template_path = 'attendance_marker/pdf1.html'
    context = {'l':l,'class_name':Class}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Class_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def ResetLocation(id):
     print("Before")
     for i in range(3600,0,-1):
        time.sleep(1)
        print(i)
     print("After")
     stu=Student.objects.get(UID=id)
     stu.class_location_x=0
     stu.class_location_y=0
     stu.save()
