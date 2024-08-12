# utils.py

#import random

#def generate_otp():
  #  return str(random.randint(100000, 999999))


import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone 
from datetime import timedelta
#from models import CustomUser




def generate_otp(self):
    otp = random.randrange(100000,999999)
    self.otp_created_at = timezone.now()  # Use timezone-aware datetime

    return otp

def send_otp_email(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    
    
def is_otp_valid(self, otp):
  if self.otp == otp and timezone.now() < self.otp_created_at + timedelta(minutes=5):
    return True
  return False    