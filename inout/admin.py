from django.contrib import admin

# Register your models here.
from .models import InoutUser,InoutUserLink

#admin.site.register(InoutUser)

@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')

@admin.register(InoutUserLink)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('inout_user','github_account','linkedin_account','city','resume','additional_info')