import pyqrcode
import png
from pyqrcode import QRCode
import hashlib
import random
from .models import Student
import time
def generate_QR(enc_key):
    s = f"https://qr-70664.web.app/student/{enc_key}"
    url = pyqrcode.create(s)
    return url.png(f"{enc_key}.png", scale = 6)
    


def generate_key(uid,name,subject,time,x,y):
    s = str(uid)+name+subject+time+str(x)+str(y)+str(random.random())
    result = hashlib.sha256(s.encode())
    
    print(result.hexdigest())
    return result.hexdigest()

def StudentIsPresent(x,y,lat1,lat2,long1,long2):
    if x>=lat1 and x<=lat2 and y>=long1 and y<=long2:
        return True
    return False





