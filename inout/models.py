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
    
    def __str__(self):
        return  self.full_name +"|"+self.school

class InoutUserLink(models.Model):
    inout_user = models.OneToOneField(InoutUser)
    github_account=models.URLField()
    #dribble_account=models.URLField(blank=True,null=True)
    #behance_account=models.URLField(blank=True,null=True)
    linkedin_account=models.URLField(blank=True,null=True)
    city=models.CharField(max_length=25)
    resume=models.FileField(upload_to='resumes')
    additional_info = models.TextField(max_length=500)

# Djano Model for registration  of Teams for InOut 3.0

class Team(models.Model):
    # Unique url id for each team to add participants and check application status.
    url_id = models.SlugField(max_length=6,primary_key=True)
    
    # Team Name
    name = models.CharField(max_length=30, unique = True)

    # Team registration date
    registration_date = models.DateTimeField(auto_now=True)

    # Team contact email
    email = models.EmailField(unique = True)

    # Application status of the Team
    application_status=models.BooleanField(default=False)
    

class Participant(models.Model):

    # T-shirt sizes
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    XLARGE = 'XL'
    XXLARGE = 'XXL'

    # T-shirt size choices
    TSHIRT_SIZE_CHOICES = ((SMALL,'Small'),(MEDIUM,'Medium'),(XLARGE,'X-Large'),(XXLARGE,'XX-Large'),) 
    
    # Participants first name
    first_name=models.CharField(max_length=25)

    # Participants last name
    last_name=models.CharField(max_length=25)
    
    # Participant email
    email = models.EmailField(unique = True)
    
    # Participant's Institute name
    school=models.CharField(max_length=80)

    # Participants graduation year
    graduation=models.DateField()

    # Participants education major
    major=models.CharField(max_length=50)

    # Participants T-shirt size
    tshirt_size=models.CharField(max_length=3,choices = TSHIRT_SIZE_CHOICES,default = SMALL)

    date_of_birth=models.DateField()
    
    gender=models.CharField(max_length=20)
    
    mobile_number=models.CharField(max_length=10)

    # Participant's city of residence
    city=models.CharField(max_length=25)
    
    # Participant's Emergency contact details
    emergency_contact_name = models.CharField(max_length=60)
    emergency_contact_phone_number = models.CharField(max_length=10)
    # Participant's GitHub Account URL
    github_account=models.URLField()
    
    # Participant's Linkedin Profile URL
    linkedin_account=models.URLField(blank=True,null=True)

    # Participant's facebook Profile URL
    facebook_account=models.URLField(blank=True,null=True)

    # Participant's twitter Profile URL
    twitter_account=models.URLField(blank=True,null=True)
    
    # Participant's resume file will be uploaded to  ./media/resumes/   
    resume=models.FileField(upload_to='resumes')
    
    # Participant's additional-info (optional)
    additional_info = models.TextField(max_length=500)

     # Participant's dietary restrictions (if any) 
    dietary_restrictions=models.CharField(max_length=50,null=True)
    
    # Participant's special needs
    special_needs=models.CharField(max_length=100,null=True,blank=True)
    
    # Participant's registration date
    registration_date = models.DateTimeField(auto_now=True)

    # Participant's Team
    team = models.ForeignKey("Team",on_delete = models.CASCADE, related_name = 'participants', related_query_name='participant')

    def _get_full_name(self):
        return self.first_name +' '+ self.last_name
    
    full_name = property(_get_full_name)
    
    
    def __str__(self):
        return  self.full_name +"|"+self.school