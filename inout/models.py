from django.db import models

from django.contrib.auth.models import User

class InoutUser(models.Model):
    participant=models.OneToOneField(User)
    first_name=models.CharField(max_length=25)
    last_name=models.CharField(max_length=25)
    graduation=models.DateField()
    major=models.CharField(max_length=50)
    shirt_size=models.CharField(max_length=20)
    dietary_restrictions=models.CharField(max_length=50,null=True)
    special_needs=models.CharField(max_length=100,null=True,blank=True)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=20)
    phone_number=models.CharField(max_length=15)
    school=models.CharField(max_length=80)
    application_status=models.BooleanField(default=False)


    def _get_full_name(self):
        return self.first_name +' '+ self.last_name
    def _get_email(self):
        return self.participant.email
    full_name = property(_get_full_name)
    email = property(_get_email)

class InoutUserLinks(models.Model):
    inout_user = models.OneToOneField(InoutUser)
    github_account=models.URLField()
    #dribble_account=models.URLField(blank=True,null=True)
    #behance_account=models.URLField(blank=True,null=True)
    city=models.CharField(max_length=25)
    resume=models.FileField(upload_to='resumes')
    additional_info = models.TextField(max_length=500)
