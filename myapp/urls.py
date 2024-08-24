from django.urls import path
from .views import RegisterView,UpdateProfileView,UpdateEmail,GenerateEmailUpdateOTP, UserLoginView, ProfileView,GenerateOTP, ChangePasswordView,UserListView,ForgotPassword
from .views import LogoutAndBlacklist
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    #path('login/', LoginView.as_view(), name='login'),
   
    path('get-all-users/', UserListView.as_view(), name='get-all-users'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('generate-otp/', GenerateOTP.as_view(), name='generate-otp'),
    path('forgot-user-password/', ForgotPassword.as_view(), name='forgot-user-password'),
        
    path('email-update-otp/', GenerateEmailUpdateOTP.as_view(), name='email-update-otp/'),
    path('update-email/', UpdateEmail.as_view(), name='update-email'),
    
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-blacklist/', LogoutAndBlacklist.as_view(), name='token_blacklist'),
     
]
    

