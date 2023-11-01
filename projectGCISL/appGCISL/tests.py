from django.test import TestCase, Client
from django import setup
from django.urls import reverse
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectGCISL.settings')
setup()

# Create your tests here.
from .models import GCISLUser, UserManager, Survey, Question, Choice, Response
from django.apps import apps
from datetime import date
GCISLUser = apps.get_model('appGCISL', 'GCISLUser')
Survey = apps.get_model('appGCISL', 'Survey')
Question = apps.get_model('appGCISL', 'Question')
Choice = apps.get_model('appGCISL', 'Choice')
Response = apps.get_model('appGCISL', 'Response')

# testing class for user creation
class TestGCISLUserCreation(TestCase):
    def setUp(self):
        manage1 = UserManager()
        manage1.create_Faculty(first_name='Johnny', last_name='T', email='johnnyt@wsu.edu', age_range='55-65', phone='3605552093', password='SomePassword$01')
        manage2 = UserManager()
        manage2.create_Resident(first_name='Ronny', last_name='T', email='ronnyt@gmail.com', age_range='55-65', phone='3605552094', password='SomePassword$02')
    
    # tests for user creation
    def test_facultyuser(self):
        # check if user is saved to database
        user = GCISLUser.objects.get(email='johnnyt@wsu.edu')
        self.assertTrue(user != None)
        self.assertTrue(user.is_Faculty)
        self.assertFalse(user.is_Resident)
    
    def test_residentuser(self):
        user2 = GCISLUser.objects.get(email='ronnyt@gmail.com')
        self.assertEqual("ronnyt@gmail.com", user2.email)
        self.assertTrue(user2 != None)
        self.assertFalse(user2.is_Faculty)
        self.assertTrue(user2.is_Resident)
    # ----------------------------------------------------
    
    def test_query_obj(self):
        # checks for existing query of all objects
        qr = GCISLUser.objects.all()
        self.assertTrue(qr.exists())

class TestSurveyViews(TestCase):
    # create a test survey with questions and choices
    def setUp(self):
        # init client for survey view tests
        self.client = Client()
        Survey.objects.update(status=False)
        # create survey for setup
        survey = Survey(title='Test Case Survey', description='Test Survey Description, happy testing!', startdate=date(year=2023, month=10, day=31), enddate=date(year=2030, month=10, day=31), status=True)
        survey.save()
        
        # create questions for setup
        question_mc = Question(surveyid=survey, questiontext='Test: Fruit?', questiontype='multiple_choice')
        question_mc.save()
        question_c = Question(surveyid=survey, questiontext='Test: Schools?', questiontype='checkbox')
        question_c.save()
        question_n = Question(surveyid=survey, questiontext='Test: Favorite Number?', questiontype='numeric')
        question_n.save()
        question_t = Question(surveyid=survey, questiontext='Test: Name?', questiontype='text')
        question_t.save()
        
        # create choices for setup
        choice1_mc = Choice(questionid=question_mc, choicetext='Apple')
        choice1_mc.save()
        choice2_mc = Choice(questionid=question_mc, choicetext='Banana')
        choice2_mc.save()
        choice3_mc = Choice(questionid=question_mc, choicetext='Orange')
        choice3_mc.save()
        choice4_mc = Choice(questionid=question_mc, choicetext='Grape')
        choice4_mc.save()
        choice1_c = Choice(questionid=question_c, choicetext='WSU')
        choice1_c.save()
        choice2_c = Choice(questionid=question_c, choicetext='UW')
        choice2_c.save()
        choice3_c = Choice(questionid=question_c, choicetext='OSU')
        choice3_c.save()
        choice4_c = Choice(questionid=question_c, choicetext='USC')
        choice4_c.save()

        # create user
        manager = UserManager()
        manager.create_Resident(first_name='Test', last_name='User', email='testuser@gmail.com', age_range='55-65', phone='3605552094', password='Password$08')
        # Authenticate the user
        self.client.login(username='testuser@gmail.com', password='Password$08')

    # test just checks to make sure the setup worked
    def test_setup(self):
        survey = Survey.objects.get(title='Test Case Survey')
        questions=Question.objects.filter(surveyid=survey)
        self.assertIsNotNone(survey)
        self.assertIsNotNone(questions)
        for question in questions:
            if question.questiontype == 'multiple_choice' or question.questiontype == 'checkbox':
                choices = Choice.objects.filter(questionid=question)
                self.assertIsNotNone(choices)
        self.assertEqual(survey, Survey.objects.get(status=True))


    def test_getSurvey(self):
        pass

    def test_postSurvey(self):
        survey = Survey.objects.get(title='Test Case Survey')
        questions=Question.objects.filter(surveyid=survey)
        post_data = {}
        # Define the URL for the view you want to test
        url = reverse('survey')  # Replace 'your_view_name' with the actual name of your view
        
        # create post request data
        for question in questions:
            # add the fields and 
            if question.questiontype == 'multiple_choice':
                post_data[f'question_{question.pk}'] = f'{Choice.objects.get(questionid=question, choicetext="Apple").pk}'
            elif question.questiontype == 'checkbox':
                post_data[f'question_{question.pk}'] = [f'{Choice.objects.get(questionid=question, choicetext="WSU").pk}', f'{Choice.objects.get(questionid=question, choicetext="UW").pk}']
            elif question.questiontype == 'numeric':
                post_data[f'question_{question.pk}'] = '8'
            else:
                post_data[f'question_{question.pk}'] = 'Test Casey'


        # Send a POST request with the example data
        response = self.client.post(url, post_data)

        responses = Response.objects.filter(surveyid=survey)

        for r in responses:
            print("Checking response")
            self.assertIsNotNone(r)

        # Perform assertions to check the redirection
        self.assertRedirects(response, reverse('get_involved'))
        
class TestAuthenticationViews(TestCase):
    def setUp(self):
        pass
    
    def test_LoginView(self):
        pass

class TestOtherViews(TestCase):
    def setUp(self):
        pass

    def test_LandingView(self):
        pass

#### Directions for writing creating coverage on command line ####
# python -m coverage run manage.py test
# coverage report
# coverage html