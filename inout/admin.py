from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import InoutUser,InoutUserLink

#admin.site.register(InoutUser)

@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')

@admin.register(InoutUserLink)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('inout_user','github_link','linkedin_account','city','resume','additional_info')

    def github_link(self, obj):
    	return format_html("<a target='_blank' href='{url}'>{url}</a>", url=obj.github_account)

    	github_link.allow_tags = True