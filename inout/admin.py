from django.contrib import admin

# Register your models here.
from .models import InoutUser,InoutUserLink

#admin.site.register(InoutUser)
admin.site.register(InoutUserLink)
@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')
