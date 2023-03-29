from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# user model, with all fields neccessary for first milestone
class UserManager(BaseUserManager):
    def create_Resident(self, firstname, lastname, usernme, email, age, ulocation, uphone, password=None):
        if not email:
            raise ValueError('Resident must have an email address.')
        if not firstname:
            raise ValueError('Resident must have first name.')
        if not lastname:
            raise ValueError('Resident must have last name.')
        if not usernme:
            raise ValueError('Resident must have a unique username.')
        
        user = GCISLUser(
            first_name=firstname,
            last_name=lastname,
            username=usernme,
            email=self.normalize_email(email),
            age_range=age,
            location=ulocation,
            phone=uphone
        )
        user.resident = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_Faculty(self, firstname, lastname, usernme, email, age, ulocation, uphone, password=None):
        if not email:
            raise ValueError('Resident must have an email address.')
        if not firstname:
            raise ValueError('Resident must have first name.')
        if not lastname:
            raise ValueError('Resident must have last name.')
        if not usernme:
            raise ValueError('Resident must have a unique username.')
        
        user = GCISLUser(
            first_name=firstname,
            last_name=lastname,
            username=usernme,
            email=self.normalize_email(email),
            age_range=age,
            location=ulocation,
            phone=uphone
        )
        user.faculty = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class GCISLUser(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=25, unique=True)
    email = models.CharField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(verbose_name= "first", max_length=30)
    last_name = models.CharField(verbose_name= "last", max_length=30)
    age_range = models.CharField(verbose_name="age", max_length=20)
    location = models.CharField(verbose_name="location", max_length=250)
    phone = models.CharField(verbose_name="phone", max_length=20)
   
   # identifiers only one can be true and false not both true, will be set when created.
    faculty = models.BooleanField(default=False)
    resident = models.BooleanField(default=False)
    #possibly use this for admin too?

    objects= UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first', 'last', 'email', 'age', 'location']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_Email(self):
        return self.email
    
    
    # checks for whether the user is resident, returns false if not
    @property
    def is_Resident(self):
        field_name = 'resident'
        obj = GCISLUser.objects.first()
        field_object = GCISLUser._meta.get_field(field_name)
        return getattr(obj, field_object.attname)
    
    # checks for whether the user is faculty, returns false if not
    @property
    def is_Faculty(self):
        field_name = 'faculty'
        obj = GCISLUser.objects.first()
        field_object = GCISLUser._meta.get_field(field_name)
        return getattr(obj, field_object.attname)