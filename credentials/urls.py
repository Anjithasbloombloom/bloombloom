# urls.py
from django.urls import path
from . import views
from allauth.account.views import SignupView
from .views  import CustomLoginView # type: ignore
from django.urls import path
from .views import CustomPasswordResetView
from .models import CustomUser
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from .views import google_oauth_callback
# from .views import update_interest






urlpatterns = [

    path('header/',views.header,name='header'),
    path('footer/',views.footer,name='footer'),
    path('test/',views.test1,name='test1'),
    path('accounts/signup/',views.signup_view, name='account_signup'),
    path('accounts/profile/',views.profile, name='profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/verify-otp/password_reset/', views.verify_otp, name='verify_otp'),
    path('accounts/reset-password/', views.reset_password, name='reset_password'),
    path('accounts/dob', views.signup_dob, name='dob'),
    path('accounts/signup_password/',views.signup_password,name='signup_password'),
    path('accounts/phone_otp/',views.phone_otp,name='phone_otp'),
    path('accounts/google/callback/', google_oauth_callback, name='google_oauth_callback'),
    path('accounts/google/default_callback/', OAuth2CallbackView, name='default_google_oauth_callback'),
    path('purpose/',views.save_top_purposes_view,name='save_top_purposes_view'),
    path('resend_otp/',views.sendOTP,name='resend_otp'),
    path('resend_otp_email/',views.sendOTPEmail,name='resend_otp_email'),
    path('interest/',views.save_top_interest_view,name='save_top_interest_view'),
    # path('update_interest/', update_interest, name='update_interest'),
    # path('update',views.update_interest,name='update_interest')



   
    # Other URLs...
]




