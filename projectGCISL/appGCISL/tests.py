from django.test import TestCase
from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectGCISL.settings')
setup()

# Create your tests here.
from .models import GCISLUser, UserManager
from django.apps import apps
GCISLUser = apps.get_model('appGCISL', 'GCISLUser')

# testing class for user creation
class TestGCISLUserCreation(TestCase):
    def setUp(self):
        manage1 = UserManager()
        manage1.create_Faculty(firstname='Johnny', lastname='T', email='johnnyt@wsu.edu', age='55-65', uphone='3605552093', password='SomePassword$01')
        manage2 = UserManager()
        manage2.create_Resident(firstname='Ronny', lastname='T', email='ronnyt@gmail.com', age='55-65', uphone='3605552094', password='SomePassword$02')
    
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