from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView, CreateView
import datetime

from psycopg2 import IntegrityError

from .models import Choice, Question, Survey
from .forms import RegistrationForm, LoginAuthForm, QuestionForm, SurveyForm, ChoiceForm, ResponseForm

# Create your views here.
# home view
# Note to Ali, to access user data, call {{ user.(datafield) }} - data fields could be the first name or other attributes
def landing_view(request):
    if request.user.is_authenticated:
        return render(request, 'landing-logged.html', {'user': request.user})
    else:
        return render(request, 'landing.html')

# Get Involved
def getinvolved_view(request):
    if request.user.is_authenticated:
        return render(request, 'getinvolved-logged.html', {'user': request.user})
    else:
        return render(request, 'getinvolved.html')

# Survey
def survey_view(request):
    return render(request, 'survey.html')

# Contact
def contact_view(request):
    if request.user.is_authenticated:
        return render(request, 'contact-logged.html', {'user': request.user})
    else:
        return render(request, 'contact.html')

# About
def about_view(request):
    if request.user.is_authenticated:
        return render(request, 'about-logged.html', {'user': request.user})
    else:
        return render(request, 'about.html')

# Register
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()     
            return redirect('login')
        else:
            messages.error(request, form.errors, form.non_field_errors())
            return redirect('register')
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'rform': form})
    

# Login
# citation: (documentation for user login that I followed) https://docs.djangoproject.com/en/4.1/topics/auth/default/
def login_view(request):
    if request.method == 'POST':
        form = LoginAuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_Resident:
                    # these will be different in future based off status
                    return redirect('landing')
                if user.is_Faculty:
                    # these will be different in future based off status
                    return redirect('landing')
            else:
                messages.error(request,'Email or password not correct!')
                return redirect('login')
        else:
            messages.error(request,'Please fill in all fields!')
            return redirect('login')
    else:
        form = LoginAuthForm()
        return render(request, 'login.html', {'lform':form})
    
def logout_view(request):
    logout(request)
    return redirect('landing')

## the view that processes new Survey creations, Question Creations, and Choice creations
def survey_faculty_view(request):
    if request.method == 'POST':
        ## check for creation of a new survey, new question, or new choice
        if 'CreateSurveyButton' in request.POST:
            sform = SurveyForm(request.POST)
            if sform.is_valid():
                # form is valid save the new survey and redirect to the new survey screen!
                sform.instance.startdate = datetime.date.today()
                survey = sform.save()
                return redirect(f'/survey-faculty/manager/{survey.surveyid}/', survey=survey)
            else:
                print(sform.errors)
        else:
            return HttpResponse('<h1>Custom Error</h1>', status=418)
    else:
        # survey gets filtered
        if 'titles' in request.GET:
            selected_survey_id = request.GET.get('titles')
            # check for None case
            if selected_survey_id != None:
                return redirect(f'/survey-faculty/manager/{selected_survey_id}')
        # normal get request to render the page
        else:
            sform = SurveyForm()
            if request.user.is_authenticated and request.user.is_staff:
                # get survey data, all questions attached, and choices that belong to the survey
                return render(request, 'survey-faculty.html', {'sform': sform})
            else:
                # user is not faculty, should not be able to view the survey customize screen!
                return render(request, 'getinvolved-logged.html')

def survey_manager_view(request, survey_id):
    if request.method == 'POST':
        ## check for creation of a new survey, new question, or new choice
        if 'CreateSurveyButton' in request.POST:
            sform = SurveyForm(request.POST)
            if sform.is_valid():
                # form is valid save the new survey and redirect to the new survey screen!
                sform.instance.startdate = datetime.date.today()
                survey = sform.save()
                return redirect(f'/survey-faculty/manager/{survey.surveyid}/', survey=survey)
            else:
                print(sform.errors)
        elif 'CreateQuestionButton' in request.POST:
            qform = QuestionForm(request.POST)
            if qform.is_valid():
                qform.instance.surveyid = Survey.objects.get(surveyid=survey_id)
                question = qform.save()
                return redirect(f'/survey-faculty/manager/{survey_id}/')
        elif 'CreateChoiceButton' in request.POST:
            cform = ChoiceForm(request.POST)
            # set current survey Id to the choice
            questionid = request.POST.get('questionid')
            # cform.instance.questionid = Question.objects.get(questionid=int(questionid))
            if cform.is_valid():
                cform.instance.questionid = Question.objects.get(questionid=int(questionid))
                choice = cform.save()
                return redirect(f'/survey-faculty/manager/{survey_id}/')
            else:
                print(cform.errors)
        else:
            return HttpResponse('<h1>Custom Error</h1>', status=418)
    else:
        # survey gets filtered
        if 'titles' in request.GET:
            selected_survey_id = request.GET.get('titles')
            # check for None case
            if selected_survey_id != None:
                return redirect(f'/survey-faculty/manager/{selected_survey_id}')
        # normal get request to render the page
        else:
            sform = SurveyForm()
            qform = QuestionForm()
            cform = ChoiceForm()
            if request.user.is_authenticated and request.user.is_staff:
                # get survey data, all questions attached, and choices that belong to the survey
                survey = getSurvey(survey_id)
                allSurveys = Survey.objects.all()
                questions = getQuestions(survey_id)
                choices = Choice.objects.all()
                return render(request, 'survey-manager.html', {'sform': sform, 'qform' : qform, 'cform' : cform, 'survey' : survey, 'questions': questions, 'choices' : choices, 'allSurveys' : allSurveys})
            else:
                # user is not faculty, should not be able to view the survey customize screen!
                return render(request, 'getinvolved-logged.html')


## helpers
# function returns survey with specific id
def getSurvey(survey_id):
    try:
        survey = Survey.objects.get(surveyid=survey_id)
        print(survey.title)
        return survey 
    except Survey.DoesNotExist:
        return None

# returns the collection of questions
def getQuestions(survey_id):
    try:
        return Question.objects.filter(surveyid=survey_id).order_by('questionid')
    except Question.DoesNotExist:
        return None

# # returns the collection of choices matching the survey and question
# def getQuestionChoices(survey_id):
#     try:
#         return Choice.objects.filter(surveyid=survey_id).order_by('choiceid')
#     except Choice.DoesNotExist:
#         return None

        

