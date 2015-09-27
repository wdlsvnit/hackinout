from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect

from django_object_actions import DjangoObjectActions

# Register your models here.
from .models import InoutUser,InoutUserLink

import sys
#admin.site.register(InoutUser)

@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')

@admin.register(InoutUserLink)
class ProfileAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display = ('inout_user','approval_status','github_link','linkedin_account','city','resume','additional_info')

    def github_link(self, obj):
    	return format_html("<a target='_blank' href='{url}'>{url}</a>", url=obj.github_account)

    github_link.allow_tags = True
    
    def approval_status(self,obj):
        return obj.inout_user.application_status
    approval_status.allow_tags = True
    def approve_user(self, request, obj):
        applicant=InoutUser.objects.get(id=obj.inout_user.id)
        applicant.application_status = True
        applicant.save()
        return HttpResponseRedirect('/admin/inout/inoutuserlink/')
    approve_user.label = "Approve"  # optional
    approve_user.short_description = "Approve user participation"  # optional

    objectactions = ('approve_user', )