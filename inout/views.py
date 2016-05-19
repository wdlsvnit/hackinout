
import base64
import hashlib
import logging
import string,random

from allaccess.views import OAuthCallback

from allaccess.compat import smart_bytes, force_text
from allaccess.compat import get_user_model
from allaccess.clients import get_client
from allaccess.compat import smart_bytes, force_text
from allaccess.compat import get_user_model
from allaccess.models import Provider, AccountAccess

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect,render
from django.views.generic import RedirectView, View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.utils.html import format_html
from django.core.mail import send_mail, BadHeaderError, send_mass_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template, render_to_string


from inout.models import InoutUser,InoutUserLink, Team
from inout.forms import InoutUserForm,TeamForm,ParticipantForm

from django.contrib.auth.decorators import login_required

from django.views.decorators.clickjacking import xframe_options_exempt
 

def get_short_code():
    '''
    This method generates a random string of length 6
    to serve as a unique id for the team registration process.

    '''
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Team.objects.get(pk=short_id)
        except:
            return short_id

def home_view(request):
    ''' 
    Home view renders the team form to start the registration process 
    and could probably serve as the home page of the site.

    '''
    if request.method =='POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.url_id = get_short_code()
            new_team.save()

            ''' 
            TODO: Send an email to the provided address
                 with the team url and other instructions.
            '''
            send_team_registration_email(new_team)
            return HttpResponseRedirect('/new/'+new_team.url_id)

        else:
            return render(request,'inout/index.html',{'form':form})
    form = TeamForm()
    return render(request,'inout/index.html',{'form':form})

def team_view(request,team_url_id):
    ''' 
        Team view should display the option to add a participant to a team if 
        number of participants is less than 3, it should also display the team status
        and the details of already registered participants.
    '''
    team = Team.objects.get(pk = team_url_id)
    participants = team.participants.all()
    if participants.count() >= 3:
        return render(request,'inout/team_view.html',{'participants':participants,'team_name':team.name})
    if request.method =='POST':
        form = ParticipantForm(request.POST,request.FILES)
        if form.is_valid():
            new_team_participant = form.save(commit=False)
            new_team_participant.team = team 
            new_team_participant.save()
            '''
            TODO : Send an email to the participant confirming the registration and other instructions.
            '''
            send_participant_registration_email(new_team_participant)
            return HttpResponseRedirect('/new/'+team_url_id)

        else:
            return render(request,'inout/team_view.html',{'form':form,'participants':participants,'team_name':team.name})
    form = ParticipantForm()
    return render(request,'inout/team_view.html',{'form':form,'participants':participants,'team_name':team.name})



def send_team_registration_email(team):
    team_name = team.name
    team_url  = team.url_id
    subject = team_name +': Registration successfull !'
    from_email = "Team InOut <"+settings.DEFAULT_FROM_EMAIL+">"
    to_email = [ team.email ]
    context = {

         "team_name": team_name,
         "team_url" : team_url,
     }

    email_template_html = "team_mail_body.html"
    email_template_txt  = "team_mail_body.txt"
    send_email(subject,from_email,to_email,email_template_html,email_template_txt,context)

def send_participant_registration_email(participant):
    participant_name = participant.full_name
    subject = participant_name +': Registration successfull !'
    from_email = "Team InOut <"+settings.DEFAULT_FROM_EMAIL+">"
    to_email = [ participant.email ]
    context = {

         "participant_name": participant_name,
     }

    email_template_html = "participant_mail_body.html"
    email_template_txt  = "participant_mail_body.txt"
    send_email(subject,from_email,to_email,email_template_html,email_template_txt,context)

def send_email(subject,from_email,to_email,email_template_html,email_template_txt,context):
    text_content = render_to_string(email_template_txt, context)
    html_content = render_to_string(email_template_html, context)
    headers = {'X-Priority':1}
    if subject and to_email and from_email :
        try:
            msg=EmailMultiAlternatives(subject, text_content, from_email, to_email,headers = headers)
            msg.attach_alternative(html_content,"text/html")
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
''' 

Below code is for the old registration process involving MLH.

'''



@xframe_options_exempt
def Index(request):
    user=request.user
    if user.is_superuser:
        return HttpResponseRedirect('/admin/')
    if user.id==None:
        return render(request,'inout/index.old.html',{'user':None,'app_status':False})
    try:
        profile_links=user.inoutuser.inoutuserlink
    except InoutUserLink.DoesNotExist:
        return HttpResponseRedirect('/accounts/profile/')
    inout_user_status=user.inoutuser.application_status
    return render(request,'inout/index.old.html',{'user':request.user,'app_status':inout_user_status})

@xframe_options_exempt
def closed(request):
        return render(request,'inout/closed.html')

@xframe_options_exempt
@login_required
def UserDash(request):
    user=request.user
    if user.is_superuser:
        return HttpResponseRedirect('/admin/')
    inout_user=user.inoutuser
    if request.method == 'POST':
        form = InoutUserForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            user_links=form.save(commit=False)
            user_links.inout_user=inout_user
            user_links.save()
            return HttpResponseRedirect('/')
    else:
        try:
            profile_links=user.inoutuser.inoutuserlink
            return HttpResponseRedirect('/')
        except InoutUserLink.DoesNotExist:
            pass
        form = InoutUserForm()

    return render(request,'inout/dashboard.html',{'user':request.user,'inout_user':inout_user,'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class CustomCallback(OAuthCallback):

    def get(self, request, *args, **kwargs):
        name = kwargs.get('provider', '')
        try:
            provider = Provider.objects.get(name=name)
        except Provider.DoesNotExist:
            raise Http404('Unknown OAuth provider.')
        else:
            if not provider.enabled():
                raise Http404('Provider %s is not enabled.' % name)
            client = self.get_client(provider)
            callback = self.get_callback_url(provider)
            # Fetch access token
            raw_token = client.get_access_token(self.request, callback=callback)
            if raw_token is None:
                return self.handle_login_failure(provider, "Could not retrieve token.")
            # Fetch profile info
            info = client.get_profile_info(raw_token)
            try:
                info=info['data']
            except KeyError:
                pass
            if info is None:
                return self.handle_login_failure(provider, "Could not retrieve profile.")
            identifier = self.get_user_id(provider, info)

            if identifier is None:
                return self.handle_login_failure(provider, "Could not determine id.")
            # Get or create access record
            defaults = {
                'access_token': raw_token,
            }
            access, created = AccountAccess.objects.get_or_create(
                provider=provider, identifier=identifier, defaults=defaults
            )
            if not created:
                access.access_token = raw_token
                AccountAccess.objects.filter(pk=access.pk).update(**defaults)
            user = authenticate(provider=provider, identifier=identifier)
            if user is None:
                return redirect('/closed')
            else:
                return self.handle_existing_user(provider, user, access, info)

    def handle_existing_user(self, provider, user, access, info):
        "Login user and redirect."

        kwargs = {
            'school':info.pop('school')['name']
        }
        info.pop('id')
        info.pop('created_at')
        info.pop('updated_at')
        info.pop('email')
        kwargs.update(info)
        inout_user=InoutUser.objects.filter(participant=user.id).update(**kwargs)

        login(self.request, user)
        return redirect(self.get_login_redirect(provider, user, access))

    def get_or_create_user(self, provider, access, info):

        "Create InOut user profile."
        kwargs = {
            'school':info.pop('school')['name']
        }
        info.pop('id')
        info.pop('created_at')
        info.pop('updated_at')
        email=info.pop('email')
        kwargs.update(info)
        new=InoutUser(**kwargs)


        digest = hashlib.sha1(smart_bytes(access)).digest()
        # Base 64 encode to get below 30 characters
        # Removed padding characters
        username = force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
        User = get_user_model()
        kwargs = {
            User.USERNAME_FIELD: username,
            'password': None,
            'email':email


        }
        new_user=User.objects.create_user(**kwargs)
        new.participant = new_user
        new.save()
        return new_user
