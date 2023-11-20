from django.contrib import admin
from .models import GCISLUser, Survey, Choice, Question, Response
from django.apps import apps
GCISLUser = apps.get_model('appGCISL', 'GCISLUser')
Survey = apps.get_model('appGCISL', 'Survey')
Question = apps.get_model('appGCISL', 'Question')
Choice = apps.get_model('appGCISL', 'Choice')
Response = apps.get_model('appGCISL', 'Response')
# Register your models here.

@admin.register(GCISLUser)
class GCISLUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestioneAdmin(admin.ModelAdmin):
    pass

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass
