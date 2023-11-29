# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# good website for understanding these forms
from django import forms
from django.forms import ModelForm, Form, CharField, PasswordInput, TextInput
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm 
from .models import GCISLUser, UserManager, Survey, Question, Choice, Response
from django.core.exceptions import ValidationError
import re

GCISLUser = apps.get_model('appGCISL', 'GCISLUser')
Survey = apps.get_model('appGCISL', 'Survey')
Question = apps.get_model('appGCISL', 'Question')
Choice = apps.get_model('appGCISL', 'Choice')
Response = apps.get_model('appGCISL', 'Response')


# create your forms here
# followed implementation from 
class RegistrationForm(UserCreationForm):
    password1 = CharField(label=("Password"),
        widget=PasswordInput  (attrs={'placeholder':'Password'}))
    password2 = CharField(label=("Password confirmation"),
        widget=PasswordInput (attrs={'placeholder':'Confirm Password'}))
    phone2 = CharField(label=("Phone2"),
        widget=TextInput(attrs={'placeholder': 'Phone Check'}))
    email2 = CharField(label=("Email"), 
        widget=TextInput(attrs={'placeholder': 'Email'}) )

    class Meta:
        model = GCISLUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'age_range']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder':('Email')})
        self.fields['last_name'].widget.attrs.update({'placeholder':('Last Initial')})    
        self.fields['first_name'].widget.attrs.update({'placeholder':('First Name')})
        self.fields['age_range'].widget.attrs.update({'placeholder':('Age Range')})       
        self.fields['phone'].widget.attrs.update({'placeholder':('Phone Number')})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        
        # Check if password contains at least one uppercase letter
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.", code='no_uppercase')

        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("Password must contain at least one special character.", code='no_special_character')
        
        return self.cleaned_data
    
    def clean_phone2(self):
        phone1 = self.cleaned_data['phone']
        phone2 = self.cleaned_data['phone2']
        if phone1 is not None and phone2 is not None and phone1 != phone2:
            raise ValidationError("Phone numbers do not match!", code='phone_mismatch')
        
        return phone1
    
    def clean_username(self):
        # username and password should be the same
        email = self.cleaned_data['email'].lower()
        user = GCISLUser.objects.get(email = email)
        if user != None:
            raise ValidationError("User with username exists.", code='user_exists')
        
        return email
    
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        
        # Check if password contains at least one uppercase letter
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.", code='no_uppercase')

        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("Password must contain at least one special character.", code='no_special_character')
        
        return password1
    
    def clean_email2(self):
        email = self.cleaned_data['email']
        email2 = self.cleaned_data['email2']

        if email is not None and email2 is not None and email != email2:
            raise forms.ValidationError("Emails do not match.", code='email_mismatch')

        return email
    

    def save(self):
        #checking for faculty email/ may use different method later but for iteration 1 this is the main method
        create = UserManager()
        if '@wsu.edu' in self.cleaned_data['email'] and self.clean_password2():
            user = create.create_Faculty(email=self.cleaned_data['email'], password=self.cleaned_data['password2'], first_name = self.cleaned_data['first_name'], last_name = self.cleaned_data['last_name'], age_range = self.cleaned_data['age_range'], phone = self.cleaned_data['phone'])
        else:
            user = create.create_Resident(email=self.cleaned_data['email'], password=self.cleaned_data['password2'], first_name = self.cleaned_data['first_name'], last_name = self.cleaned_data['last_name'], age_range = self.cleaned_data['age_range'], phone = self.cleaned_data['phone'])
        return user

class LoginAuthForm(Form):
    email = CharField(label="Email Address", widget=TextInput (attrs={'placeholder':'Email Address'}))
    password = CharField(label="Password", widget=PasswordInput(attrs={'placeholder':'Password'}))

class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'startdate', 'enddate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'custom-input'})
        self.fields['enddate'].widget=forms.DateInput(attrs={'type': 'date'})

class QuestionForm(ModelForm):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text'),
        ('checkbox', 'Checkbox'),
        ('numeric', 'Numeric')
        # Add more choices as needed
    ]

    questiontype = forms.ChoiceField(choices=QUESTION_TYPE_CHOICES)  # Add a CSS class for styling

    class Meta:
        model = Question
        fields = ['surveyid', 'questiontext', 'questiontype']

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['questionid', 'choicetext']

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['surveyid', 'questionid', 'respondentname', 'respondentemail', 'responsetext', 'responsenumeric', 'choiceid']