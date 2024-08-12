from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models, transaction
from datetime import timedelta
from .utils import generate_otp
from django.utils import timezone 
import random
from django.contrib.admin.models import LogEntry
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    username=None
    mobile_number = models.CharField(max_length=10)
    email=models.EmailField(unique=True,null=False)
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    address = models.TextField()
    otp = models.CharField(max_length=10, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )

    def __str__(self):
        return self.email

    # 
    
    def set_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()  # Use timezone-aware datetime
        self.save()
        
        return self.otp

    def is_otp_valid(self, otp):
        if self.otp == otp and timezone.now() < self.otp_created_at + timedelta(minutes=5):
            return True
        return False
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Delete related admin log entries
            LogEntry.objects.filter(user_id=self.id).delete()
            super().delete(*args, **kwargs)
            
            
class CustomUserLogs(models.Model):
    useremail=models.EmailField(unique=False)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp field here=
    password_changed_date=models.DateTimeField(auto_now_add=True)   
    
    def is_valid(self):
        # Optional: Add logic to check if OTP is still valid (e.g., 5 min expiration)
        pass
    
    


    
