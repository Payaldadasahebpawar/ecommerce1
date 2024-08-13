from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
import re
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import CustomUser
#Register Serializer

from django.core.validators import RegexValidator

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
       
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','email','mobile_number','address','gender','profile_image','password','confirm_password']
    
    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters")
        return value
    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters")
        return value
    
    def validate_mobile_number(self, value):
        if not value.isdigit()and len(value) == 10: 
            raise serializers.ValidationError("Mobile number accept only digits")
       # return value
       
        if not len(value) == 10:  
            raise serializers.ValidationError("Mobile number should be 10 digits")
        
        if CustomUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if any(char.isupper() for char in value):
            raise ValidationError("Email address should not contain uppercase letters.")
    
        return value  
    
    def validate_password(self, value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("The password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one number.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?' for char in value):
            raise serializers.ValidationError("The password must contain at least one special symbol.")

        return value
    
   
    def create(self, validated_data):
               
        if validated_data['password']==validated_data['confirm_password']:
            user = CustomUser(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
               # username=validated_data['username'],
                email=validated_data['email'],
                mobile_number=validated_data['mobile_number'],
                address=validated_data['address'],
                gender=validated_data['gender'], 
                # profile_image=validated_data['profile_image'],
            )
            
            user.save()    
            return user
        
        raise serializers.ValidationError({"password": "Password fields didn't match."})
 

#Login serializer
# User = get_user_model()

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)


#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
        
#         print(email,password)

#         if email and password:
#             # Authenticate the user
#             user = authenticate(request=self.context.get('request'), email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError("Invalid email or password.")
#         else:
#             raise serializers.ValidationError("Must include 'email' and 'password'.")
        
#         data['user'] = user
#         return data

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     def validate(self, validated_data):
#         email=validated_data['email']
#         password=validated_data['password']
        
#         print(email,password)
        
#         # user = authenticate(email=email,password=password)
#         user = authenticate(request=self.context.get('request'), email=email, password=password)
#         print(user)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Invalid credentials")


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
     
    class Meta:
        model = CustomUser
        fields = ['email','password']

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        
        print(email,password)

        if email and password:
            user = CustomUser.objects.get(email=email)
           
            if user:
                if user.is_active:
                    return user
                else:
                    raise serializers.ValidationError("User is not active.")
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include both username and password.")

#User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'email', 'mobile_number', 'gender', 'profile_image', 'address')
  
class EmailUpdateSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value  
     
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','mobile_number', 'profile_image', 'address']

    def validate_mobile_number(self, value):
        """
        Validate that the mobile number is exactly 10 digits.
        """
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("The mobile number must be exactly 10 digits.")
        return value

    def validate_first_name(self, value):
        """
        Validate that the first name contains only characters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("The first name must contain only alphabetic characters.")
        return value

    def validate_last_name(self, value):
        """
        Validate that the last name contains only characters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("The last name must contain only alphabetic characters.")
        return value

    def update(self, instance, validated_data):
        """
        Update the user profile.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance
   
# for email verification

class UpdateEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

#verify OTP

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    new_email = serializers.EmailField()

class CustomUserSerializerUpdate(serializers.ModelSerializer):
    
    otp=serializers.CharField(required=True)
    class Meta:
        model=CustomUser
        fields = ['email'] 
# FPasswordSerilizer
class FPasswordSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(required=True,max_length=10)
    Confirm_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("The password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one number.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?' for char in value):
            raise serializers.ValidationError("The password must contain at least one special symbol.")

        return value
    class Meta:
         model=CustomUser
         fields=['otp','email','new_password','Confirm_password']
                       
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        # Check if the new password is different from the old password
        if self.initial_data.get('old_password') == value:
            raise serializers.ValidationError("The new password must not be the same as the old password.")

        # Validate the new password according to Django's built-in validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        # Check if the new password contains at least one uppercase, lowercase, number, and special symbol
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The new password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("The new password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The new password must contain at least one number.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?' for char in value):
            raise serializers.ValidationError("The new password must contain at least one special symbol.")

        return value

    def validate(self, data):
        # Check if the new password and confirm new password match
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("The new password and confirm new password do not match.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
     
class UpdateEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate_new_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if not user.is_otp_valid(data['otp']):
            raise serializers.ValidationError("Invalid or expired OTP.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.email = self.validated_data['new_email']
        user.save()
        return user
        