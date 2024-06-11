from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth import authenticate, login
import random
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from allauth.account.views import LoginView,PasswordResetView
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import OAuth2CallbackView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from .models import User_detail
from django.contrib.auth.decorators import login_required
from .models import Purpose, User_detail,Interest,AddEducation

from django.http import HttpResponse
from django.shortcuts import render
from course_app.models import Course
from course_app.models import Stage
# from .models import Language,Location,Mode,Authors,Collaborators,Topics,Producers,Sponsors
from django.shortcuts import redirect,get_object_or_404
# from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


def header(request):
    return render(request,'header.html')

def footer(request):
    return render(request,'footer.html')

phone_regex = r'^\+?1?\d{9,15}$'
name_regex = r'^[a-zA-Z\s]+$'
phone_validator = RegexValidator(
    regex=phone_regex,
    message='Enter a valid phone number.'
)
name_validator = RegexValidator(
    regex=name_regex,
    message='Enter a valid name.'
)

def signup_view(request):
    errors = {}
    if request.method == 'POST':
        try:
            name_validator(request.POST['name'])
            name = request.POST['name']
        except ValidationError:
            errors['name'] = 'name is invalid'
        try:
            validate_email(request.POST['email'])
            email = request.POST['email']
            if CustomUser.objects.filter(email=email).exists():
                errors['registered email'] = 'email is already registered'
        except ValidationError:
            errors['email'] = 'email is invalid'
        try:
            phone_validator(request.POST['number'])
            number = request.POST['number']
            if CustomUser.objects.filter(phone_number=number).exists():
                errors['registered number'] = 'number is already registered'
        except ValidationError:
            errors['number'] = 'phone number is invalid'
        if not errors:
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            #new
            sendOTP(request)
            return render(request, 'accounts/phone_otp.html', {'message': number})
        return render(request, 'accounts/signup.html', {'errors': errors})
    else:
        if request.user.is_authenticated:
            social_accounts = SocialAccount.objects.filter(user=request.user)
            if social_accounts.exists():
                return redirect('accounts/profile')
            else:
                return redirect('socialaccount_signup')
        return render(request, 'accounts/signup.html')

def sendOTP(request):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(otp)
    request.session['phone_otp'] = otp
    message = f'Your OTP is: {otp}'
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # client.messages.create(
    #     to=request.session['number'],
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     body=message
    # )
    return render(request, 'accounts/phone_otp.html', {'message': request.session.get('number')})

def phone_otp(request):
    if request.method=='POST':
          otp=request.POST['digit1']+request.POST['digit2']+request.POST['digit3']+request.POST['digit4']+request.POST['digit5']+request.POST['digit6']
          if request.session.get('phone_otp')==otp:
            return redirect('signup_password')
    return render(request,'accounts/phone_otp.html')

def signup_password(request):
    if request.method=='POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            request.session['password']=make_password(password)
            return redirect('dob')
        return render(request, 'accounts/signup_password.html', {'message':"passwords don't match. try again"})
    return render(request,'accounts/signup_password.html')

def signup_dob(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        try:
            date_of_birth = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        except ValueError:
            pass
        modified_post = request.POST.copy()
        modified_post['date_of_birth'] = date_of_birth
        modified_post['username'] = request.session.get('name')
        modified_post['email'] = request.session.get('email')
        modified_post['password1'] = request.session.get('password')
        modified_post['password2'] = request.session.get('password')
        modified_post['phone_number'] = request.session.get('number')
        print("dbsjbjbd")
        user=CustomUser.objects.create(date_of_birth=date_of_birth, email=request.session.get('email'),username=request.session.get('name'), password=request.session.get('password'), phone_number=request.session.get('number'), location=request.session.get('location'))
            
                # Authenticate and login the user
        user = authenticate(request, email=request.session.get('email'), password=request.session.get('password'))
        print("hgcbcbv",user)
        if user is not None:
            login(request, user)
        
        return redirect('save_top_purposes_view')
    return render(request, 'accounts/dob.html')


    #     form = CustomUserCreationForm(modified_post)
    #     if form.is_valid():
    #         form.save()
    #         #new
    #         user = authenticate(request, email=request.session.get('email'), password=request.session.get('password'))
    #         if user is not None:
    #             login(request, user)
    #         return redirect('save_top_purposes_view')
    # else:
    #     form = CustomUserCreationForm()
    # return render(request, 'accounts/dob.html',{'form':form})
    # return render(request, 'accounts/dob.html')


@login_required
def save_top_purposes_view(request):
    if request.method == 'POST':
        selected_purpose_ids = request.POST.get('selected_purposes').split(',')[:5]  # Limit to top 5 purposes
        if selected_purpose_ids:
            user = request.user
            if user:
                user_detail, created = User_detail.objects.get_or_create(user=user)
                user_detail.purposes.clear()
                for purpose_id in selected_purpose_ids:
                    purpose = Purpose.objects.get(id=int(purpose_id))
                    user_detail.purposes.add(purpose)
                    # print(user_detail.purposes)
                return redirect('save_top_interest_view')
    purposes = Purpose.objects.all()
    return render(request, 'accounts/purposes.html', {'purposes': purposes})


# @login_required
# def save_top_interest_view(request):
#     if request.method == 'POST':
#         selected_interests_data = request.POST.get('selected_interests')
#         if selected_interests_data:
#             selected_interest_ids = selected_interests_data.split(',')[:3]
#             user = request.user
#             if user:
#                 user_detail, created = User_detail.objects.get_or_create(user=user)
#                 user_detail.interests.clear()
#                 for interest_id in selected_interest_ids:
#                     try:
#                         interest = Interest.objects.get(id=int(interest_id))
#                         user_detail.interests.add(interest)
#                     except Interest.DoesNotExist:
#                         # Handle the case when the interest with the specified ID does not exist
#                         pass  # You can log the error or perform other actions as needed
#                 return redirect('profile')
#         # If selected_interests data is missing or empty, handle it gracefully
#         # Redirect or render an error message as needed
#     interests = Interest.objects.all()
#     return render(request, 'accounts/interest.html', {'interests': interests})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Interest, User_detail

@login_required
def save_top_interest_view(request):
    user = request.user
    user_detail, created = User_detail.objects.get_or_create(user=user)

    if request.method == 'POST':
        selected_interests_data = request.POST.get('selected_interests')
        if selected_interests_data:
            selected_interest_ids = selected_interests_data.split(',')[:3]
            user_detail.interests.clear()
            for interest_id in selected_interest_ids:
                try:
                    interest = Interest.objects.get(id=int(interest_id))
                    user_detail.interests.add(interest)
                except Interest.DoesNotExist:
                    pass
            return redirect('test1')

    interests = Interest.objects.all()
    selected_interests = user_detail.interests.all()
    return render(request, 'accounts/interest.html', {
        'interests': interests,
        'selected_interests': selected_interests,
    })




def profile(request):
    return render(request,'accounts/profile.html')


#Modified code for login using normal way and social authenticaation
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('save_top_interest_view')  # Default success URL

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'accounts/profile.html', {'username': user.username})
        else:
            return super().post(request, *args, **kwargs)  # If normal login fails, fall back to default behavior
        
def google_oauth_callback(request):
    # Extract user data returned by Google OAuth
    user_data = request.user.socialaccount.extra_data
    
    # Print/log the user data to inspect its contents
    print("User Data from Google OAuth:", user_data)
    
    # Further processing of user data and authentication
    # Example: Redirect to another page after successful authentication

    keys = user_data.keys()
    print("Keys in User Data:", keys)
    return redirect('profile')
 
class CustomPasswordResetView(PasswordResetView):
    template_name='accounts/login_forgot password.html'
    def form_valid(self, form):
        email=form.cleaned_data['email']
        #new
        self.request.session['email']=email
        if CustomUser.objects.filter(email=email).exists():
            #new
            sendOTPEmail(self.request)
            return render(self.request, 'accounts/otp_verification.html')
        else:
            message={'message':'email address does not exist. Try another one'}
            return render(self.request, 'accounts/otp_verification.html',{'message':message['message']})
        
def sendOTPEmail(request):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    email=request.session['email']
    send_mail(
        'Password Reset OTP',
        f'Your OTP is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    request.session['reset_otp'] = otp
    return render(request, 'accounts/otp_verification.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp=request.POST['digit1']+request.POST['digit2']+request.POST['digit3']+request.POST['digit4']+request.POST['digit5']+request.POST['digit6']
        #entered_otp = request.POST.get('otp')
        reset_otp = request.session.get('reset_otp')
        print(entered_otp, reset_otp)
        if entered_otp == reset_otp:
            return render(request,'accounts/custom_password_reset.html')
        else:
            return HttpResponseBadRequest("Incorrect OTP. Please try again.")
    return render(request, 'accounts/otp_verification.html')

def reset_password(request):
    if request.method=='POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            email=request.session.get('email')
            user = CustomUser.objects.get(email=email)
            hashed_password = make_password(password)
            user.password=hashed_password
            user.save()
            #new
            user=authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
        else:
            message={'message':'the 2 passwords should match, try again'}
            return render(request, 'accounts/custom_password_reset.html', {'message':message['message']})
    return redirect('profile')

# signal newuser creation in user_detail table
@receiver(post_save, sender=CustomUser)
def user_added(sender, instance, created, **kwargs):
    if created:
         if not User_detail.objects.filter(user_id=CustomUser.objects.last().id).exists():
                User_detail.objects.create(user_id=CustomUser.objects.last().id)

def test(request):
    return render(request,'test.html')

# @login_required
# def test1(request):
#     try:
#         # Get the current user's User_detail object
#         user_detail = User_detail.objects.get(user=request.user)
#     except User_detail.DoesNotExist:
#         # If User_detail does not exist for the authenticated user, handle it gracefully
#         return redirect('profile') 
#     # Assuming User_detail exists, proceed with the rest of the code
#     interest_whole = Interest.objects.all()
#     interests_selected = user_detail.interests.all()
#     interest_whole = interest_whole.exclude(id__in=interests_selected)
#     return render(request, 'accounts/test1.html', {'user_detail': user_detail, 'interest_whole': interest_whole})

# @login_required
# def test1(request):
#     if request.method == 'POST':
#         user = request.user
#         print(User_detail.objects.get(user=request.user))
#         try:
#             user_detail = User_detail.objects.get(user=request.user)  # Assuming there is a one-to-one relationship between CustomUser and User_detail
#         except User_detail.DoesNotExist:
#             user_detail = User_detail.objects.create(user=user)
        
#         print("User Detail:", user_detail)
        
        # Retrieve form data
        # school_name = request.POST.get('schoolName')
        # degree = request.POST.get('degree')
        # field_of_study = request.POST.get('fieldOfStudy')
        # # start_date = request.POST.get('startDate')
        # month = request.POST.get('startDate')
        # year = request.POST.get('startDateYear')
        # print("month",request.POST)
        # day=1
        # start_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        # month = request.POST.get('endDate')
        # year = request.POST.get('endDateYear')
        # day=1
        # end_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        
        # Validate form data
        # if not school_name or not degree or not field_of_study or not start_date:
        #     return HttpResponseBadRequest("Missing required fields")
        
        # Save education information
    #     addeducation = AddEducation.objects.create(
    #         user_detail=user_detail,
    #         school=school_name,
    #         degree=degree,
    #         field_of_study=field_of_study,
    #         start_date=start_date,
    #         end_date=end_date
    #     )
        
    #     return redirect('profile')

    # else:    
    #     user = request.user
    #     user_detail, created = User_detail.objects.get_or_create(user=user)
    #     interests = Interest.objects.all()
    #     selected_interests = user_detail.interests.all()

    # return render(request, 'accounts/test1.html', {
    #     'interests': interests,
    #     'selected_interests': selected_interests,
    # })




# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from django.http import JsonResponse

# @login_required

# @login_required
# def update_interest(request):
#     if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         interest_id = request.POST.get('interest_id')
#         selected = request.POST.get('selected') == 'true'
#         try:
#             interest = Interest.objects.get(id=interest_id)
#             user_detail = User_detail.objects.get(user=request.user)
#             if selected:
#                 user_detail.interests.add(interest)
#                 print("gfggggggggg",user_detail.interests)
#             else:
#                 user_detail.interests.remove(interest)
#                 print("remove",user_detail.interests)
#             return JsonResponse({'success': True})
#         except (Interest.DoesNotExist, User_detail.DoesNotExist) as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': 'Invalid request'})






from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import User_detail, AddEducation, Interest

@login_required
def test1(request):
    if request.method == 'POST':
        user = request.user
        print(User_detail.objects.get(user=request.user))
        
        try:
            user_detail = User_detail.objects.get(user=request.user)
        except User_detail.DoesNotExist:
            user_detail = User_detail.objects.create(user=user)
        
        print("User Detail:", user_detail)
        
        # Retrieve form data
        school_name = request.POST.get('schoolName')
        degree = request.POST.get('degree')
        field_of_study = request.POST.get('fieldOfStudy')
        
        # Start date
        month = request.POST.get('startDate')
        year = request.POST.get('startDateYear')
        day = 1
        
        try:
            start_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        except (ValueError, TypeError):
            start_date = None
        
        # End date
        month = request.POST.get('endDate')
        year = request.POST.get('endDateYear')
        
        try:
            end_date = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        except (ValueError, TypeError):
            end_date = None
        
        # Validate form data
        if not school_name or not degree or not field_of_study or not start_date or not end_date:
            return HttpResponseBadRequest("*indicates required")
        
        # Save education information
        addeducation = AddEducation.objects.create(
            user_detail=user_detail,
            school=school_name,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date
        )
        
        return redirect('profile')

    else:    
        user = request.user
        user_detail, created = User_detail.objects.get_or_create(user=user)
        interests = Interest.objects.all()
        selected_interests = user_detail.interests.all()

    return render(request, 'accounts/test1.html', {
        'interests': interests,
        'selected_interests': selected_interests,
    })






