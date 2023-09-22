# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# good website for understanding these forms
from django.forms import ModelForm, Form, CharField, PasswordInput, TextInput
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm 
from .models import GCISLUser, UserManager, Survey, Question, Choice, Response
from django.core.exceptions import ValidationError, 

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

    def check_phone(self):
        phone1 = self.cleaned_data['phone']
        phone2 = self.cleaned_data['phone2']
        if phone1 == phone2:
            return True
        else:
            return False
    
    def username_clean(self):
        # username and password should be the same
        email = self.cleaned_data['email2'].lower()
        user = GCISLUser.objects.filter(email = email)
        if user.count():
            return False
        else:
            return True

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self):
        #checking for faculty email/ may use different method later but for iteration 1 this is the main method
        create = UserManager()
        if '@wsu.edu' in self.cleaned_data['email'] and self.clean_password2() and self.username_clean():
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

class QuestionForm(ModelForm):
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
