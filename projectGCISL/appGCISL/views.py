from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView, CreateView
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Survey, Response
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
    # You need to get the survey with the given ID
    try:
        survey = Survey.objects.get(status=True)
        
    except Survey.DoesNotExist:
        raise Http404("Survey does not exist")

    questions = getQuestions(survey)  # You need to get questions for this survey

    # Count the number of questions
    count = len(questions)

    # Get choices for each question
    choices = {}
    for question in questions:
        choices[question.questionid] = filter_choice(question.questionid)

    # Create response forms for each question
    rforms = [ResponseForm({'surveyid': survey, 'respondentname': request.user.first_name + " " + request.user.last_name, 'respondentemail': request.user.email}) for _ in range(count)]

    if request.method == "POST":
        # Handle form submissions (map responses to the database responses)
        mapResponses(request, questions, choices)
        return render(request, 'survey-submit.html')

    # Check user's authentication and role
    if request.user.is_authenticated:
        if request.user.is_resident:
            return render(request, 'survey.html', {'survey': survey, 'questions': questions, 'choices': choices, 'rforms': rforms})
        elif request.user.is_staff:
            redirect('set_active_survey', survey_id=survey.pk)
    
    return HttpResponse("User doesn't have privileges.")


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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
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
                return redirect(f'/survey/editor/{survey.surveyid}/', survey=survey)
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
                return redirect(f'/survey/editor/{selected_survey_id}')
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
                return redirect(f'/survey/editor/{survey.surveyid}/', survey=survey)
            else:
                print(sform.errors)
        if 'Set-Active-Button' in request.POST:
            set_active_survey(request, survey_id)
            return redirect(f'/survey/editor/{survey_id}/')
        elif 'CreateQuestionButton' in request.POST:
            # create new question form with request data
            qform = QuestionForm(request.POST)
            # validate and save the form
            if qform.is_valid():
                qform.instance.surveyid = Survey.objects.get(surveyid=survey_id)
                question = qform.save()
                return redirect(f'/survey/editor/{survey_id}/')
        elif 'CreateChoiceButton' in request.POST:
            choicetext = ""
            # get the question with the text input and get the text from that choice
            questionGroup = Question.objects.filter(surveyid = survey_id)
            for question in questionGroup:
                if request.POST.get(f'choicetext_{question.pk}') != '':            
                    choicetext = request.POST.get(f'choicetext_{question.pk}')
                    # check to make sure choice passed in correctly
                    if choicetext != None:
                        choice = Choice(questionid = question, choicetext = choicetext)
                        choice.save()
            return redirect(f'/survey/editor/{survey_id}/')
        elif 'DeleteQuestion' in request.POST:
            # look for deleteQuestion value in POST request
            # get all the questions in the survey
            question = Question.objects.get(questionid = int(request.POST.get('DeleteQuestion')))
            #make sure question != None else return the error
            if question is None:
                return HttpResponse('Error, question to delete not found!', status=418)
            else:
                question.delete()
                return redirect(f'/survey/editor/{survey_id}/')
        else:
            return HttpResponse('<h1>No correct button was clicked.</h1>', status=418)
    else:
        # survey gets filtered
        if 'titles' in request.GET:
            selected_survey_id = request.GET.get('titles')
            # check for None case
            if selected_survey_id != None:
                return redirect(f'/survey/editor/{selected_survey_id}')
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

def survey_landing_view(request):
    if request.method == 'GET':
        surveys = Survey.objects.all()
        return render(request, 'survey-landing.html', {'surveys': surveys})
    # button clicks will be post requests
    elif request.method == 'POST':
        if 'DeleteSurvey' in request.POST:
            # delete survey button has been selected
            pass

def response_view(request, survey_id):
    if request.method == 'POST':
        return HttpResponse('<h1>Custom Error</h1>', status=418)
    else:
        # survey gets filtered
        if 'titles' in request.GET:
            selected_survey_id = request.GET.get('titles')
            # check for None case
            if selected_survey_id != None:
                return redirect(f'/survey/editor/{selected_survey_id}/response')
        # normal get request to render the page
        else:
            if request.user.is_authenticated and request.user.is_staff:
                # get survey data, all questions attached, and choices that belong to the survey
                responses = Response.objects.all()
                survey = getSurvey(survey_id)
                allSurveys = Survey.objects.all()
                questions = getQuestions(survey_id)
                choices = Choice.objects.all()
                return render(request, 'responses.html', {'responses':responses, 'survey' : survey, 'questions': questions, 'choices' : choices, 'allSurveys' : allSurveys})
            else:
                # user is not faculty, should not be able to view the survey customize screen!
                return render(request, 'getinvolved-logged.html')

def set_active_survey(request, survey_id):
    # Just decided to embed it into the survey manager view to help
    if survey_id:
        try:
            selected_survey = Survey.objects.get(pk=survey_id)
            Survey.objects.exclude(pk=survey_id).update(status=False)
            selected_survey.status = True
            selected_survey.save()
            return selected_survey
        except Survey.DoesNotExist:
            raise Http404("Survey does not exist")
    else:
        return HttpResponse("Invalid survey ID.")
    

# def your_view_function(request):
#     # Retrieve the active survey
#     active_survey = Survey.objects.filter(status=True).first()

#     # Pass the active survey to the template
#     return render(request, 'getinvolved-logged.html', {'active_survey': active_survey})

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

def getCurrentSurvey():
        today = datetime.datetime.now().date()
        surveys = Survey.objects.all()
        for survey in surveys:
            d2 = datetime.datetime.strptime(str(survey.enddate.day)+"/"+str(survey.enddate.month)+"/"+str(survey.enddate.year), "%d/%m/%Y").date()
            if d2 > today:
                # date is valid return current survey
                return survey
        # case where no surveys are valid return None
        return None

def mapQuestionsToResponseForms(rforms, questions):
    # iterate each form assigning the form a  specific questionid
    if rforms != None and questions != None:
        formIter = iter(rforms)
        for question in questions:
            rform = next(formIter)
            rform.fields['questionid'].initial = question
        return rforms
    else:
        return None


# # returns the collection of choices matching the survey and question
# def getQuestionChoices(survey_id):
#     try:
#         return Choice.objects.filter(surveyid=survey_id).order_by('choiceid')
#     except Choice.DoesNotExist:
#         return Node

def filter_choice(questionid):
    filter_choice = []
    for choice in Choice.objects.all():
        if choice.questionid.pk == questionid:
            filter_choice.append(choice)
    return filter_choice

# this function recieves the answers from the users and saves them once the form is submitted
def mapResponses(request, questions, choice_dict):
    # check which choice was picked in each question
    checkbox_string = ""
    for question in questions:
        # check for text answer, if it is get the answer and save to response
        if question.questiontype == "text":
            text_answer = request.POST.get(f'question_{question.pk}')
            response = Response(surveyid=question.surveyid, questionid=question, respondentname = request.user.last_name + ", " + request.user.first_name,  respondentemail=request.user.email, responsetext=text_answer)
            response.save()
        elif question.questiontype == "checkbox":
            checkbox_string = ""
            choices = request.POST.getlist(f'question_{question.pk}')
            for choice in choices:
                selected_choice = Choice.objects.get(choiceid=int(choice))
                if selected_choice != None:
                    checkbox_string = checkbox_string + selected_choice.choicetext + ", "
            if checkbox_string != "":
                response = Response(surveyid=question.surveyid, questionid=question, respondentname = request.user.last_name + ", " + request.user.first_name,  respondentemail=request.user.email, responsetext=checkbox_string)
                response.save()
        elif question.questiontype == "multiple_choice":
                if f'question_{question.pk}' in request.POST:
                    # get the choice from the db
                    choicet = Choice.objects.get(choiceid=int(request.POST.get(f'question_{question.pk}')))
                    response = Response(surveyid=question.surveyid, questionid=question, respondentname = request.user.last_name + ", " + request.user.first_name,  respondentemail=request.user.email, responsetext=choicet.choicetext, choiceid=choicet)
                    response.save()
                else:
                    return Exception("Multiple choice not answered.")
        else:
            # numeric
            if f'question_{question.pk}' in request.POST:
                num = request.POST.get(f'question_{question.pk}')
                response = Response(surveyid=question.surveyid, questionid=question, respondentname = request.user.last_name + ", " + request.user.first_name,  respondentemail=request.user.email, responsenumeric=int(num))
                response.save()
    return