from django import forms
from django.contrib.auth.forms import UserCreationForm 
from models import GCISLUser

# create your forms here
class RegistrationForm(UserCreationForm):
    class Meta:
        model = GCISLUser
        fields = ['email', 'first_name', 'last_name', 'phone']

class LoginForm(forms.Form):
    username = forms.EmailField('Username/Email', max_length=60, help_text="Please enter username/email.")
    password = forms.CharField('Password', help_text="Please enter email/username to login.")
    