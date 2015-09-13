from django.contrib import admin

# Register your models here.
from .models import InoutUser,InoutUserLinks

#admin.site.register(InoutUser)
admin.site.register(InoutUserLinks)
@admin.register(InoutUser)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name','application_status','email')
