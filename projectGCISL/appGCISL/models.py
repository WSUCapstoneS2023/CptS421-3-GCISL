from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# user model, with all fields neccessary for first milestone
class UserManager(BaseUserManager):
    def create_Resident(self, firstname, lastname, email, age, uphone, password=None):
        if not email:
            raise ValueError('Resident must have an email address.')
        if not firstname:
            raise ValueError('Resident must have first name.')
        if not lastname:
            raise ValueError('Resident must have last name.')
        
        user = GCISLUser(
            first_name=firstname,
            last_name=lastname,
            email=self.normalize_email(email),
            age_range=age,
            phone=uphone,
            resident=True,
            faculty=False
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_Faculty(self, firstname, lastname, email, age, uphone, password=None):
        if not email:
            raise ValueError('Resident must have an email address.')
        if not firstname:
            raise ValueError('Resident must have first name.')
        if not lastname:
            raise ValueError('Resident must have last name.')
        
        user = GCISLUser(
            first_name=firstname,
            last_name=lastname,
            email=self.normalize_email(email),
            age_range=age,
            phone=uphone,
            faculty=True,
            resident=False
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class GCISLUser(AbstractBaseUser):
    # unique needs to be false considering email and user must be same
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    
    first_name = models.CharField(verbose_name= "first", max_length=30)
    last_name = models.CharField(verbose_name= "last", max_length=30)
    
    # added age choices for age range
    class Ages(models.TextChoices):
        FIRST = "1", "55-65"
        SECOND = "2", "66-75"
        THIRD = "3", "75+"
    
    age_range = models.CharField(verbose_name="age", choices=Ages.choices, max_length=10)
    phone = models.CharField(verbose_name="phone", max_length=20)
    # profile picture for the user profile
    image = models.ImageField(default='/static/assets/general/icon.png', upload_to='static/assets/general/')

   # identifiers only one can be true and false not both true, will be set when created.
    faculty = models.BooleanField(default=False)
    resident = models.BooleanField(default=False)

    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first', 'last', 'age', 'phone']

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