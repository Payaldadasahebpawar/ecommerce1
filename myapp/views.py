from datetime import datetime
import datetime
from django_filters import rest_framework as filters
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from random import randint
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from .models import CustomUser,CustomUserLogs
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from .serializers import UpdateEmailSerializer,UserSerializer,TokenSerializer
from .serializers import UserLoginSerializer,FPasswordSerilizer,UpdateProfileSerializer
from .serializers import EmailUpdateSerializer,ChangePasswordSerializer,RegisterSerializer
from .utils import generate_otp, send_otp_email
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
  
class CustomPagination(PageNumberPagination):
    page_size = 5  # Define page size
    page_size_query_param = 'page_size'
    max_page_size = 100
     
User = get_user_model()

class RegisterView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]    
    
    def post(self, request, *args, **kwargs):
        print(request.data)  # Log the request data
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
             user = serializer.save()
             return Response(data={'message': 'User created Successfully.','status':'Success',"code": 201,"content_type":"null","error": {},'data': serializer.data,}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = []
       
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        token_serializer = TokenSerializer(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        token_serializer.is_valid()
        return Response(token_serializer.data, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user   
    
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check if the old password is correct
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["The old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

            # Save the new password
            serializer.save()

            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    filterset_fields = ['email','mobile_number','first_name','last_name','gender', 'is_active']   
    # search_fields = ['email','mobile_number','first_name','last_name','gender', 'is_active']
    authentication_classes = []  # No authentication required
    permission_classes = []
                      
class GenerateOTP(APIView):
    permission_classes=[]
    def post(self, request):
        emailotp = generate_otp(self)
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email) 
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        print(emailotp)
        CustomUserLogs.objects.create(useremail=email,otp=emailotp)
        send_otp_email(email,emailotp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)

class ForgotPassword(APIView):
    serilizer=FPasswordSerilizer
    def put(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')
        new_password=request.data.get('new_password')
        Confirm_password=request.data.get('Confirm_password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
       
        userlog = CustomUserLogs.objects.last()
        print(otp,userlog.otp,type(otp),type(userlog))
        if otp == userlog.otp and timezone.now() < userlog.password_changed_date + datetime.timedelta(minutes=5):
        # if otp==userlog.otp and timezone.now()<userlog.password_changed_date+datetime.timedelta(seconds=45):
                
            if new_password==Confirm_password:
                user.set_password(new_password)
                user.save()                
                return Response({'sucessfuly changed':'corret otp'},status=status.HTTP_201_CREATED)
            return Response({'error':'password does not match'})
        else:
            return Response({'error':'new_password and Confirm_password mismatch'})
    
class UpdateProfileView(generics.UpdateAPIView): 
    # pagination_class = StandardResultsSetPagination              
    queryset = CustomUser.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RegisterSerializer(snippet)
        #return Response(serializer.data)
        return Response(data={'data': serializer.data,'message': 'data reterive Successfully.','status':'Success'}, status=status.HTTP_200_OK)


    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UpdateProfileSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'data': serializer.data, 'message': 'data Updated Successfully.','status':'HTTP_200_OK'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        # snippet = self.get_object(pk)
        snippet = CustomUser.objects.get(pk=pk)
        snippet.is_active = False
        snippet.save()
        
        return Response({ 'message': 'data Deleted Successfully.','status':'Success','code':'204'}, status=status.HTTP_204_NO_CONTENT)

        
    
    
    
    

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = RegisterSerializer(snippet)
    #     snippet.delete()
    #     return Response(data={'data':serializer.data,'message':'data deleted Successfully.','status':'Success'},status=status.HTTP_204_NO_CONTENT)

class GenerateEmailUpdateOTP(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        otp = user.set_otp()

        # Send OTP via email
        send_mail(
            'Your OTP for email update',
            f'Your OTP is {otp}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your current email."}, status=status.HTTP_200_OK)

class UpdateEmail(APIView):
    def put(self, request, *args, **kwargs):
        serializer = UpdateEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Token blacklisted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

