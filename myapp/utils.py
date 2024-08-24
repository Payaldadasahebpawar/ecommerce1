# utils.py

#import random

#def generate_otp():
  #  return str(random.randint(100000, 999999))
import datetime
import random
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone 
from datetime import timedelta
from .models import CustomUserLogs

def generate_otp(self):
  # otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
  otp = "123456"  # Generate a 6-digit OTP
  #otp_uui = str(uuid.uuid4())          # Generate a UUID
  # otp_created_at = datetime.now()       # Record the OTP creation time
  # otp_expiry_time = otp_created_at + timedelta(minutes=10)  # Set OTP expiry time (optional)
  return otp #otp_created_at ,, otp_expiry_time

  # otp = random.randrange(100000,999999)
  #   self.otp_uuid = uuid.uuid4()
  #   self.otp_created_at = timezone.now()  # Use timezone-aware datetime
  #   return otp

def send_otp_email(email, otp):
    subject = 'Your OTP for Forgot Password'
    message = f'Your OTP is: {otp}' 
    # message=f'your uuid:{otp_uuid}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    # CustomUserLogs.objects.create(useremail=email,otp=otp)#,password_changed_date=otp_expiry_time)

    send_mail(subject, message, from_email, recipient_list)
    
    
def validate_otp(user_otp, user_otp_created_at):
    current_time = datetime.now()
    otp_expiry_time = user_otp_created_at + timedelta(minutes=5)  # Assume OTP expires in 10 minutes
    
    if current_time > otp_expiry_time:
        return False, "OTP expired"
    return True, "OTP is valid"    
    
    
# def is_otp_valid(self, otp):
#   if self.otp == otp and timezone.now() < self.otp_created_at + timedelta(minutes=5):
#     return True
#   return False    


# import random
# import uuid
# from datetime import datetime, timedelta

# def generate_otp():
#     otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
#     otp_uuid = str(uuid.uuid4())          # Generate a UUID
#     otp_created_at = datetime.now()       # Record the OTP creation time
#     otp_expiry_time = otp_created_at + timedelta(minutes=10)  # Set OTP expiry time (optional)
    
#     return otp, otp_uuid, otp_created_at, otp_expiry_time

# def validate_otp(user_otp, user_otp_created_at):
#     current_time = datetime.now()
#     otp_expiry_time = user_otp_created_at + timedelta(minutes=10)  # Assume OTP expires in 10 minutes
    
#     if current_time > otp_expiry_time:
#         return False, "OTP expired"
#     return True, "OTP is valid"

