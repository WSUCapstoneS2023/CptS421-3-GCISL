from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

# Create your models here.
# user model, with all fields neccessary for first milestone
class UserManager(BaseUserManager):
    def create_Resident(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = GCISLUser(email=email, **extra_fields)
        user.is_resident = True
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_Faculty(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = GCISLUser(email=email, **extra_fields)
        user.is_resident = False
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        if "@wsu.edu" not in email:
            raise ValidationError("Email is not a Washington State Univeristy email, please use a staff Washington State University email.")
        
        if not GCISLUser.objects.filter(email=email).exists() :
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_Faculty(email, password, **extra_fields)
        else:
            if not GCISLUser.objects.get(email).is_Resident:
                user = GCISLUser.objects.get(email)
                user.is_superuser = True
                return user


class GCISLUser(AbstractBaseUser,PermissionsMixin):
    # unique needs to be false considering email and user must be same
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, )
    
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
    is_staff = models.BooleanField(default=False)
    is_resident = models.BooleanField(default=False)

    # date user joined
    date_joined = models.DateTimeField(auto_now_add=True)

    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age_range', 'phone']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_Email(self):
        return self.email
    
    # checks for whether the user is resident, returns false if not
    @property
    def is_Resident(self):
        return self.is_resident
    
    # checks for whether the user is faculty, returns false if not
    @property
    def is_Faculty(self):
        return self.is_staff
    
class Choice(models.Model):
    ChoiceID = models.AutoField(primary_key=True)  # Primary key, auto-generated
    QuestionID = models.IntegerField()  # Foreign key to the Question table (adjust field type as needed)
    ChoiceText = models.TextField()  # Text field for the choice text

    def __str__(self):
        return self.ChoiceText  # String representation of the choice

    class Meta:
        db_table = 'Choice'  # Specify the database table name
        
class Response(models.Model):
    survey_id = models.IntegerField()
    question_id = models.IntegerField() 
    respondent_name = models.CharField(max_length=255)
    respondent_email = models.EmailField(max_length=255)
    response_text = models.TextField()
    response_numeric = models.IntegerField()
    choice_id = models.IntegerField()
    
    def __str__(self):
        return f"Response by {self.respondent_name}"  # String representation of the response
    
    class Meta:
        db_table = 'Response'  # Specify the database table name
    
    
