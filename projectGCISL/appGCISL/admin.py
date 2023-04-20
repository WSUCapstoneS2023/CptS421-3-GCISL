from django.contrib import admin
from .models import GCISLUser
from django.apps import apps
GCISLUser = apps.get_model('appGCISL', 'GCISLUser')
# Register your models here.

@admin.register(GCISLUser)
class GCISLUserAdmin(admin.ModelAdmin):
    pass