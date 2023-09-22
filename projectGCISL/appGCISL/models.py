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
    
class Survey(models.Model):
    SurveyID = models.IntegerField(verbose_name='survey_id', primary_key=True)
    Title = models.CharField(verbose_name='title', max_length=255)
    Description = models.TextField(verbose_name='description')
    StartDate = models.DateTimeField(verbose_name='start_date')
    EndDate = models.DateTimeField(verbose_name='end_date')

    def str(self):
        return f"Response by {self.Title}"  # String representation of the response

    class Meta:
        db_table = 'Survey'  # Specify the database table name

class Question(models.Model):
    QuestionID = models.IntegerField(verbose_name='question_id', primary_key=True)
    SurveyID = models.ForeignKey("Survey", on_delete=models.SET_NULL)
    QuestionText = models.TextField(verbose_name='question_text')
    QuestionType = models.TextChoices("Multiple Choice", "Text", "Numeric")

    def str(self):
        return f"Response by {self.QuestionText}"  # String representation of the response

    class Meta:
        db_table = 'Question'  # Specify the database table name

class Choice(models.Model):
    ChoiceID = models.AutoField(verbose_name='choice_id',primary_key=True)  # Primary key, auto-generated
    QuestionID = models.ForeignKey("Question", on_delete=models.SET_NULL)  # Foreign key to the Question table (adjust field type as needed)
    ChoiceText = models.TextField(verbose_name='choice_text', null=False)  # Text field for the choice text

    def str(self):
        return self.ChoiceText  # String representation of the choice

    class Meta:
        db_table = 'Choice'  # Specify the database table name

class Response(models.Model):
    SurveyID = models.ForeignKey("Survey", on_delete=models.SET_NULL)
    QuestionID = models.ForeignKey("Question", on_delete=models.SET_NULL) 
    RespondentName = models.CharField(verbose_name='respondent_name', max_length=255)
    RespondentEmail = models.EmailField(verbose_name='respondent_email',max_length=255)
    ResponseText = models.TextField(verbose_name='response_text')
    ResponseNumeric = models.IntegerField(verbose_name='response_numeric')
    ChoiceID = models.ForeignKey("Choices", on_delete=models.SET_NULL)

    def str(self):
        return f"Response by {self.RespondentName}"  # String representation of the response

    class Meta:
        db_table = 'Response'  # Specify the database table name
