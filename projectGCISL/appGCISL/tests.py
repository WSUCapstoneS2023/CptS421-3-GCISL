from unittest import TestCase
from appGCISL.models import GCISLUser, UserManager

# Create your tests here.
class GCISLUserTestCases(TestCase):
    def setUp(self):
        manage = UserManager()
        manage.create_Faculty(firstname='Johnathan', lastname='T', email='johnathant@wsu.edu', age='55-65', uphone='3605552093', password='SomePassword$01')
    
    def test_user(self):
        # check if user is saved to database
        user = GCISLUser.objects.get(first_name='Johnathan')
        self.assertTrue(user != None)
        self.assertTrue(user.is_Faculty)
        self.assertFalse(user.is_Resident)