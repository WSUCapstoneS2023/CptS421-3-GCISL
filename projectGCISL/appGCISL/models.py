from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# user model, with all fields neccessary for first milestone
class UserManager(BaseUserManager):
    def create_Resident(self, firstname, lastname, phonenum, email, password=None):
        if not email:
            raise ValueError('Resident must have an email address.')
        if not firstname:
            raise ValueError('Resident must have first name.')
        if not lastname:
            raise ValueError('Resident must have last name.')
        if not phonenum:
            raise ValueError('Resident must have phone number.')
        
        user = self.model(
            first_name=firstname,
            last_name=lastname,
            phone=phonenum,
            email=self.normalize_email(email),
        )
        user.resident = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_Faculty(self, firstname, lastname, phonenum, email, password=None):
        if not email:
            raise ValueError('Faculty must have an email address.')
        if not firstname:
            raise ValueError('Faculty must have first name.')
        if not lastname:
            raise ValueError('Faculty must have last name.')
        
        user = self.model(
            first_name=firstname,
            last_name=lastname,
            phone=phonenum,
            email=self.normalize_email(email),
        )
        user.faculty = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class GCISLUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(verbose_name= "first", max_length=30)
    last_name = models.CharField(verbose_name= "last", max_length=30)
    phone = models.CharField(unique= True, max_length=10, help_text="Enter phone number, example: 1234567890")
   
   # identifiers only one can be true and false not both true, will be set when created.
    faculty = models.BooleanField(default=False)
    resident = models.BooleanField(default=False)

    #possibly use this for admin too?

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first', 'last']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_Email(self):
        return self.email
    
    
    # checks for whether the user is resident, returns false if not
    @property
    def is_Resident(self):
        return self.resident
    
    # checks for whether the user is faculty, returns false if not
    @property
    def is_Faculty(self):
        return self.faculty