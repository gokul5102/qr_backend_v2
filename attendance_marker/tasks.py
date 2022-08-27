from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_QR,StudentIsPresent,generate_key
from .models import Attendance,Student,Class_details
import os
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives

BASE_DIR = Path(__file__).resolve().parent.parent

@shared_task(bind=True)
def send_mail_func(self,subject,time,room_no):
    stu=Student.objects.all()
    c=Class_details.objects.get(room_no=room_no)
    for i in stu:
            uid = i.UID
            stu_x=i.class_location_x
            stu_y=i.class_location_y
            print(uid,' ',StudentIsPresent(stu_x,stu_y,c.lat_1,c.lat_2,c.long_1,c.long_2))
            if StudentIsPresent(stu_x,stu_y,c.lat_1,c.lat_2,c.long_1,c.long_2):
                enc_key=generate_key(uid,i.name,subject,time,c.lat_1,c.long_1)
                a=Attendance.objects.create(student=i,encoded_string=enc_key,subject=subject,time_of_lecture=time)
                a.save()
                generate_QR(enc_key)
                s, from_email, to = "Your attendance for today\'s lecture", settings.EMAIL_HOST_USER, i.email
                text_content = 'Please mark your attendance.'
                html_content = '<p>Please <strong>mark your attendance</strong></p>'
                msg = EmailMultiAlternatives(s, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                image=f"{enc_key}.png"
                file_path = os.path.join(BASE_DIR,image)
                with open(file_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<{name}>'.format(name=image))
                    img.add_header('Content-Disposition', 'inline', filename=image)
                msg.attach(img)
                msg.send()
    return "Done"


