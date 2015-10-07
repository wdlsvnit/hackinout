from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
# from django.core.mail import send_mail, BadHeaderError, send_mass_mail
# from django.conf import settings
from django.template.loader import get_template, render_to_string

from django_object_actions import DjangoObjectActions

# Register your models here.
from .models import InoutUser,InoutUserLink

import os
import sys
#admin.site.register(InoutUser)

@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')

@admin.register(InoutUserLink)
class ProfileAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display = ('inout_user','approval_status','github_link','linkedin_link','city','resume','additional_info')

    def github_link(self, obj):
    	return format_html("<a target='_blank' href='{url}'>{url}</a>", url=obj.github_account)
    def linkedin_link(self, obj):
    	return format_html("<a target='_blank' href='{url}'>{url}</a>", url=obj.linkedin_account)

    github_link.allow_tags = True
    linkedin_link.allow_tags = True

    def approval_status(self,obj):
        return obj.inout_user.application_status
    approval_status.allow_tags = True
    def approve_user(self, request, obj):
        applicant=InoutUser.objects.get(id=obj.inout_user.id)
        applicant.application_status = True
        applicant.save()

        # first_name = applicant.first_name
        # subject = 'InOut Registration approved!'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # to_email = [ applicant.email ]
        # context = {
        #     "first_name": first_name,
        # }
        # email_template_html = "mail_body.html"
        # email_template_txt  = "mail_body.txt"
        # text_content = render_to_string(email_template_txt, context)
        # html_content = render_to_string(email_template_html, context)

        # if subject and to_email and from_email :
        #     try:
        #         send_mail(subject, text_content, from_email, to_email, fail_silently=False, html_message=html_content)
        #     except BadHeaderError:
        #         return HttpResponse('Invalid header found.')

        return HttpResponseRedirect('/admin/inout/inoutuserlink/')
    approve_user.label = "Approve"  # optional
    approve_user.short_description = "Approve user participation"  # optional

    objectactions = ('approve_user', )