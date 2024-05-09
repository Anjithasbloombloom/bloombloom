from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import LoginForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email','phone_number','date_of_birth','location')

        def clean_email(self):
            email = self.cleaned_data['email']
            # Check if the email already exists in the database
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
            return email

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Remove password fields
    #     del self.fields['password1']
    #     del self.fields['password2']

        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        return cleaned_data



class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
