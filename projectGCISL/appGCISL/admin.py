from django.contrib import admin
from appGCISL.models import GCISLUser
# Register your models here.
@admin.register(GCISLUser)
class GCISLUserAdmin(admin.ModelAdmin):
    pass