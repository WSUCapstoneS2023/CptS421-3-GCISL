from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import GCISLUser, UserManager

# create your forms here
# followed implementation from 
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput  (attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput (attrs={'placeholder':'Confirm Password'}))
    
    class Meta:
        model = GCISLUser
        fields = ['email', 'first_name', 'last_name', 'username', 'phone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email')})
        self.fields['last_name'].widget.attrs.update({'placeholder':('Last Initial')})        
        self.fields['first_name'].widget.attrs.update({'placeholder':('First Name')})
        # self.fields['age_range'].widget.attrs.update({'placeholder':('Age Range')})
        # self.fields['location'].widget.attrs.update({'placeholder':('Location')})        
        self.fields['phone'].widget.attrs.update({'placeholder':('Phone Number')})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self):
        if '@wsu.edu' in self.cleaned_data.get('email'):
            user = UserManager().create_Faculty(self.cleaned_data.get('first_name'), self.cleaned_data.get('last_name'), self.cleaned_data.get('username'), self.cleaned_data.get('email'), "None", "None", self.cleaned_data.get('phone'), self.cleaned_data.get('password2'))
        else:
            user = UserManager().create_Resident(self.cleaned_data.get('first_name'), self.cleaned_data.get('last_name'), self.cleaned_data.get('username'), self.cleaned_data.get('email'), "None", "None", self.cleaned_data.get('phone'), self.cleaned_data.get('password2'))
        return user

class LoginAuthForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput (attrs={'placeholder':'Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    