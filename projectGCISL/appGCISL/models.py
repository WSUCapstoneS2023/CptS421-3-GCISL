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
        FIRST = "1", "<55"
        SECOND = "2", "55-65"
        THIRD = "3", "66-75"
        FOURTH = "4", "75+"
    
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
    surveyid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'survey'

class Question(models.Model):
    questionid = models.AutoField(primary_key=True)
    surveyid = models.ForeignKey('Survey', on_delete=models.CASCADE, db_column='surveyid', blank=True, null=True)
    questiontext = models.TextField()
    questiontype = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'question'
        

class Choice(models.Model):
    choiceid = models.AutoField(primary_key=True)
    questionid = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='questionid', blank=True, null=True)
    choicetext = models.TextField()

    class Meta:
        db_table = 'choice'

class Response(models.Model):
    responseid = models.AutoField(primary_key=True)
    surveyid = models.ForeignKey('Survey', on_delete=models.CASCADE, db_column='surveyid', blank=True, null=True)
    questionid = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='questionid', blank=True, null=True)
    respondentname = models.CharField(max_length=255, blank=True, null=True)
    respondentemail = models.CharField(max_length=255, blank=True, null=True)
    responsetext = models.TextField(blank=True, null=True)
    responsenumeric = models.IntegerField(blank=True, null=True)
    choiceid = models.ForeignKey('Choice', on_delete=models.CASCADE, db_column='choiceid', blank=True, null=True)

    class Meta:
        db_table = 'response'