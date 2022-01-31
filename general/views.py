from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from general import forms as gforms
from django.core.exceptions import ObjectDoesNotExist
from general import models as gmodels
from random import random
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from general.tokens import account_activation_token
import smtplib
import socket
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
import datetime
import os
import base64
from django.forms import ModelForm
from django.conf import settings
from django import forms
import datetime
from allauth.account.views import AjaxCapableProcessFormViewMixin
from django.contrib.auth.decorators import login_required
from random import random
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.template import loader
from django.http import JsonResponse
from django.urls import reverse_lazy
from allauth.account import forms as allauthforms
from django.core.mail import send_mail
from partners import views as pviews
from partners import models as pmodels
from ipware import get_client_ip
import geoip2.database
import requests
import json
from partners.email_sender import sendmail,sendBirthday

allObject = {}

def logrequest(request,memberid=''):
    hostname = socket.gethostname()
    ip_1 = socket.gethostbyname(hostname)
    ip_2, is_routable = get_client_ip(request)
    if ip_2 is None:
        pass
    else:
        # We got the client's IP address
        if is_routable:
            pass
            # The client's IP address is publicly routable on the Internet
        else:
            pass
            # The client's IP address is private
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip_3 = s.getsockname()[0]
    except Exception:
        ip_3 = '127.0.0.1'
    finally:
        s.close()
    try:
        response = requests.get('https://api.ipify.org').text
    # result  = response.json()
        location = response
    except Exception:
        location=''
    requestlog = pmodels.VisitorsLog.objects.create(memberid=memberid, url = request.path,ip_1=ip_1,ip_2=ip_2,ip_3=ip_3,host_name=hostname,location=location)
    return True


def inherit(request, *args, **kwargs):
    allObject={}
    try:
        settings = list(gmodels.General.objects.all())[0]
    except IndexError:
        settings =[]
    allObject['settings'] = settings
    allObject['homecardarticles'] = gmodels.CardArticle1.objects.all()
    allObject['server_timestamp'] = round(datetime.datetime.now().timestamp())
    allObject['socials'] = list(gmodels.SocialLink.objects.all())

    return allObject


def gallery(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/gallery.html'
    page = request.GET.get('page', 1)

    allObject['page'] = page
    content = loader.render_to_string(template_name,allObject,request)
    template_name = 'frontend/gallery.html'
    return render(request,template_name,allObject)



def gallerycontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/gallery_content.html'
    gallery = list(gmodels.Gallery.objects.all())
    gallery.sort(key=lambda x: x.date_time_added,reverse=True)
    page = request.GET.get('page')
    paginator = Paginator(gallery, 8)
    try:
        gallery = paginator.get_page(page)
    except PageNotAnInteger:
        gallery = paginator.get_page(1)
    except EmptyPage:
        gallery = paginator.get_page(paginator.num_pages)
    allObject['gallery'] = gallery

    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)

def momentoftruth(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/moment_of_truth.html'
    content = loader.render_to_string(template_name,allObject,request)
    return render(request,template_name,allObject)


def momentoftruthcontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/moment_of_truth_content.html'
    tvs = list(pmodels.TvStation.objects.all())
    allObject['tvs'] = tvs
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)



def upcomingevents(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/upcoming_events.html'
    content = loader.render_to_string(template_name,allObject,request)
    return render(request,template_name,allObject)


def upcomingeventscontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/upcoming_events_content.html'
    upcomingevents = list(pmodels.Event.objects.all())
    upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
    allObject['upcomingevents'] =upcomingevents    
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)





def pastevents(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/past_events.html'
    content = loader.render_to_string(template_name,allObject,request)
    return render(request,template_name,allObject)


def pasteventscontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/past_events_content.html'
    pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
    pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['pastevents'] =pastevents
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)





def videos(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/videos.html'
    content = loader.render_to_string(template_name,allObject,request)
    return render(request,template_name,allObject)


def videoscontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'frontend/videos_content.html'
    videos = list(pmodels.Video.objects.all())
    videos.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['latestvideo'] = videos[0]
    allObject['videos'] =videos
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)



def home(request, *args, **kwargs):
    if request.user.is_superuser:
        redirecturl = redirect('admin_dashboard')
    else:
        partner = pmodels.DpMembers.objects.get(user=user)
        logrequest(request,partner.member_no or '')
        redirecturl = redirect('partner_dashboard')
    return redirecturl

def slideshow(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    slideshows = gmodels.SlideShow.objects.all()
    allObject['slideshows'] = slideshows
    template_name = 'frontend/slideshow.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)



def galleryhome(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    gallery = list(gmodels.Gallery.objects.all())
    gallery.sort(key=lambda x: x.date_time_added,reverse=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(gallery, 7)
    try:
        gallery = paginator.page(page)
    except PageNotAnInteger:
        gallery = paginator.page(1)
    except EmptyPage:
        gallery = paginator.page(paginator.num_pages)
    allObject['gallery'] = gallery
    template_name = 'frontend/home_gallery.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)


def sendmessage(request, *args, **kwargs):
    allObject= inherit(request, *args, **kwargs)
    if request.method == 'POST':
        newmessage = str(request.POST.copy().get('message'))
        fullname = str(request.POST.copy().get('name'))
        phonenumber = str(request.POST.copy().get('phonenumber'))
        email = str(request.POST.copy().get('email'))
        message = gmodels.ContactMessage.objects.create(name=fullname,email=email,number=phonenumber,message=newmessage)
        message.refresh_from_db()
        subject = 'New Message'
        current_site = Site.objects.get_current()


        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [message.email, ] 
        message = render_to_string('frontend/new_message.html', {
                'message': message,
            })
        send_mail( subject, message, email_from, recipient_list ) 
        template_name = 'frontend/success.html'
        allObject['message'] = 'Your Message was sent successfully'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
            'sent':True,
            'content':content,
                            }
        return JsonResponse(output_data)


def kingdomstrategieshome(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    videos = list(pmodels.Video.objects.all())
    videos.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['latestvideo'] = videos[0]
    # allObject['videos'] =videos
    articles = list(pmodels.Article.objects.all())
    articles.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['latestarticle'] = articles[0]
    articles.remove(articles[0])
    allObject['articles'] =articles
    template_name = 'frontend/home_kingdom_strategies.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)


def events(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
    upcomingevents.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['upcomingevents'] =upcomingevents
    pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
    pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['pastevents'] =pastevents
    template_name = 'frontend/events.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return JsonResponse(output_data)



def pastorsdesk(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    pastorsdesk = list(gmodels.PastorsDesk.objects.all())[0]
    allObject['pastorsdesk'] = pastorsdesk

    template_name = 'frontend/pastors_desk.html'
    return render(request,template_name,allObject)


def contactus(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)

    template_name = 'frontend/contact.html'
    return render(request,template_name,allObject)


def kingdomstrategies(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    allObject['pastorsdesk'] = pastorsdesk
    videos = list(pmodels.Video.objects.all())
    videos.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['latestvideo'] = videos[0]
    videos.remove(videos[0])
    allObject['videos'] =videos
    articles = list(pmodels.Article.objects.all())
    articles.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['articles'] =articles
    template_name = 'frontend/kingdom_strategies.html'
    return render(request,template_name,allObject)



@login_required
def unsuspend(request, *args, **kwargs):
    user = User.objects.get(username = request.user.username)
    try:
        partner = pmodels.DpMembers.objects.get(user=user)
        partner.briefly_suspended = False
        partner.suspension_count =0
        partner.save()
        output_data = {
            'partner':True,
            'unsuspended':True,
                            }
        return JsonResponse(output_data)
    except ObjectDoesNotExist:
        partner = pmodels.DpMembers.objects.get(user=user)
        partner.briefly_suspended = False
        partner.suspension_count = 0
        partner.save()
        output_data = {
            'partner':True,
            'unsuspended':True,
                            }
        return JsonResponse(output_data)



# @login_required
# def home(request, *args, **kwargs):
#     user = User.objects.get(username = request.user.username).pk
#     try:
#         partner = pmodels.DpMembers.objects.get(user=user)
#         partner = True
#         return cviews.home(request, *args, **kwargs)
#     except ObjectDoesNotExist:
#         partner = pmodels.DpMembers.objects.get(user=user)
#         partner=True 
#         return cviews.home(request, *args, **kwargs)    


@login_required
def accept_privacy_terms(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    user = User.objects.get(username = request.user.username)
    partner = pmodels.DpMembers.objects.get(user=user)
    allObject['title']='DPG | Privacy, Terms and Conditions'
    if request.method == 'POST':
        partner.privacy_terms_accepted = True
        partner.save()
        return redirect('partner_dashboard')
    else:
        if request.GET.get('next'):
            allObject['next_page']=request.GET.get('next')
            allObject['redirect_url']=''.join(tuple(request.GET.get('next')))
        template_name = 'allauth/account/privacy_terms.html'
        return render(request,template_name,allObject)
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'content':content,
                        }
        return JsonResponse(output_data)



def memberlookup(request, *args, **kwargs):
    auth.logout(request)
    # if request.user.is_authenticated:
    #     logout(request)
    #     return redirect('account_login')
    allObject = inherit(request, *args, **kwargs)
    allObject['title']='DPG | Login In'
    admin = False
    if request.method == 'POST':
    #form =allauthforms.LoginForm(request.POST)
    #if form.is_valid():
        uniqueidentifier = request.POST.copy().get('identifier').lower()
        try:
            profile = pmodels.DpMembers.objects.get(phone_no=uniqueidentifier)
        except ObjectDoesNotExist:
            try:
                profile = pmodels.DpMembers.objects.get(email_addres=uniqueidentifier)
            except ObjectDoesNotExist:
                try:
                    profile = pmodels.DpMembers.objects.get(phone_no_alt=uniqueidentifier)
                except ObjectDoesNotExist:
                    try:
                        admin = User.objects.get(username = uniqueidentifier)
                        admin= True
                    except ObjectDoesNotExist:
                        output_data = {
                            'invalid':True,
                            'error':'Record not found. Try another Phone number or Email'
                        }
                        return JsonResponse(output_data)
        if not admin:
            try:
                profile.user
                try:
                    user = User.objects.get(username=profile.user.username)
                except ObjectDoesNotExist:
                    allObject['identifier']=uniqueidentifier
                    allObject['profile']=profile

                    allObject['profile']=profile
                    template_name = 'allauth/account/create_password.html'
                    content = loader.render_to_string(template_name,allObject,request)
                    output_data = {
                                'form_content':content,
                            }
                    return JsonResponse(output_data)
            except Exception:
                allObject['identifier']=uniqueidentifier
                allObject['profile']=profile

                allObject['profile']=profile
                template_name = 'allauth/account/create_password.html'
                content = loader.render_to_string(template_name,allObject,request)
                output_data = {
                            'form_content':content,
                        }
                return JsonResponse(output_data)
        
        else: 
            if request.POST.copy().get('next'):
                allObject['next_page']=request.POST.copy().get('next')
        allObject['redirect_url']=request.POST.copy().get('next')
        allObject['identifier']=uniqueidentifier

        template_name = 'allauth/account/enter_password.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                    'form_content':content,
                }
        return JsonResponse(output_data)
        login(request, user)   
        member = True
        allObject = inherit(request)
        member = pmodels.Member.objects.get(user=user,dependant=False)
        member = True
        template_name = 'members/dashboard.html'
        content = loader.render_to_string(template_name,allObject,request)
        if request.POST.copy().get('next'):
                redirectinstance= redirect(request.POST.copy().get('next'))
        output_data = {
                            'logged_in':True,
                            'url':redirectinstance.url
                        }
        return JsonResponse(output_data)



    else:
        form = allauthforms.LoginForm()
        allObject['form'] = form
        if request.GET.get('next'):
            allObject['next_page']=request.GET.get('next')
            allObject['redirect_url']=''.join(tuple(request.GET.get('next')))
        template_name = 'allauth/account/member_lookup.html'
        return render(request,template_name,allObject)
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'content':content,
                        }
        return JsonResponse(output_data)




def membersignup(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)

    if request.method == 'POST':
        uniqueidentifier = request.POST.copy().get('identifier').lower()
        password = request.POST.copy().get('password')
        try:
            profile = pmodels.DpMembers.objects.get(phone_no__contains=uniqueidentifier)
        except ObjectDoesNotExist:
            try:
                profile = pmodels.DpMembers.objects.get(email_addres=uniqueidentifier)
            except ObjectDoesNotExist:
                try:
                    profile = pmodels.DpMembers.objects.get(phone_no_alt__contains=uniqueidentifier)
                except ObjectDoesNotExist:
                    pass
        formerrors = []
        try:
            user= User.objects.get(username=uniqueidentifier)
            formerrors.append("<li class='text-sm uk-text-bold'>Username/Phone number already taken</li>")

        except ObjectDoesNotExist:
            try:
                user= User.objects.get(email=uniqueidentifier)
                formerrors.append("<li class='text-sm uk-text-bold'>Email already taken</li>")

            except ObjectDoesNotExist:
                pass
        if formerrors:
            erroroutput ="<ul class='text-danger p-0'>"
            errorlist = ''
            for error in formerrors:
                errorlist += '<li>' +str(error)+'</li>'
            erroroutput += errorlist + '</ul>'
            output_data = { 
                            'invalid':True,
                            'modal_notification':'<b>Ooops... Something is wrong!</b>' + erroroutput,
                            
                        }
            return JsonResponse(output_data)
        harshed_password = make_password(password)
        user = User.objects.create(password=harshed_password, username=uniqueidentifier, 
        first_name =profile.first_name,last_name= profile.last_name, email= profile.email_addres or 'none')
        user.refresh_from_db()
        user.is_active = True
        user.save()
        
        # form.user_id = user_id
        chars = '0123456789' 
        token = ''
        for num in range(0,len(chars)):
            token = token +chars[round((random()-0.5)*len(chars))]
        token = token[0:6]
        profile.last_token = make_password(token)
        profile.userid = profile.member_no
        profile.user = user
        profile.save()
        # exist = True
        # while exist:
        #     nums = '0123456789'
        #     tempnums = ''
        #     lalph = 'abcdefghijklmnopqrstuvwxyz'
        #     templalph=''
        #     ualph = lalph.upper()
        #     tempualph = ''

        #     for num in range(0,len(nums)):
        #         tempnums +=nums[round((random()-0.5)*len(nums))]
        #     for num in range(0,len(lalph)):
        #         templalph +=lalph[round((random()-0.5)*len(lalph))]
        #     for num in range(0,len(ualph)):
        #         tempualph +=ualph[round((random()-0.5)*len(ualph))]
        #     firstletter= user.first_name[0].upper()
        #     lastletter =user.last_name[0].upper()
        #     temporary_userid = tempnums[0:3] + templalph[0:3]+tempualph[0:3]+firstletter+lastletter
        #     userid= []
        #     for char in temporary_userid:
        #         userid.insert(round(random()*5),char)
        #     userid = ''.join(userid)
        #     userid = 'D'+userid
        #     try:                
        #         pmodels.DpMembers.objects.get(member_no=userid)

        #     except ObjectDoesNotExist:
        #         profile.userid = profile.member_no
        #         profile.member_no = userid
        #         profile.save()
        #         exist = False
        #         break
        if profile.email_addres != '' and profile.email_addres !='none@gmail.com':
            subject = 'Account Activation - Dominion Partners Global'
            current_site = Site.objects.get_current()

            message = render_to_string('allauth/account/email_confirm.html', {
                    'token': token,
                    'user':user,
                    'settings':allObject['settings']
                })
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [user.email, ]
            sendmail(recipient_list,message,message,subject)

            # try:
            #     send_mail( subject, message, email_from, recipient_list,html_message=message )
            # except socket.gaierror:
            #     pass
            # except smtplib.SMTPServerDisconnected:
            #     pass
            subject = 'Login Details - DPG'
            current_site = Site.objects.get_current()
            message = render_to_string('allauth/account/default_password.html', {
                    'password': password,
                    'username': user.username,
                    'email':user.email,
                    'user':user
                })
            recipient_list = [user.email, ]
            sendmail(recipient_list,message,message,subject)

            # try:
            #     send_mail( subject, message, email_from, recipient_list,html_message=message )
            # except socket.gaierror:
            #     pass
            # except smtplib.SMTPServerDisconnected:
            #     pass
        user.is_active = True
        user.save()
        login(request, user)
        allObject = inherit(request)
        # member = pmodels.Member.objects.get(user=user)
        # member = True
        # template_name = 'partners/dashboard.html'
        # content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'url':redirect('accept_privacy_terms').url,
                        }
        return JsonResponse(output_data)




def loginuser(request, *args, **kwargs):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST.copy().get('username').lower()
        raw_password = request.POST.copy().get('password')
        try:
            user = User.objects.get(username=username,is_active=True)
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(email=username,is_active=True)
            except ObjectDoesNotExist:
                output_data = {
                    'invalid':True,
                    'modal_notification':'Invalid login details'
                }
                return JsonResponse(output_data)
        user = authenticate(username=user.username, password=raw_password)
        if user:
            login(request, user)
        else:
            output_data = {
            'invalid':True,
            'modal_notification':'Invalid password'
                }
            return JsonResponse(output_data)
        # allObject = inherit(request)
        # template_name = 'partners/dashboard.html'
        # content = loader.render_to_string(template_name,allObject,request)
        if request.POST.copy().get('next'):
            if request.POST.copy().get('next') == '/':
                if user.is_superuser:
                    redirecturl = redirect('admin_dashboard').url
                else:
                    partner = pmodels.DpMembers.objects.get(user=user)
                    logrequest(request,partner.member_no or '')
                    redirecturl = redirect('partner_dashboard').url

            else:
                redirectinstance= redirect(request.POST.copy().get('next'))
                redirecturl = redirectinstance.url
        else:
            if user.is_superuser:
                redirecturl = redirect('admin_dashboard').url
            else:
                partner = pmodels.DpMembers.objects.get(user=user)
                logrequest(request,partner.member_no or '')

                redirecturl = redirect('partner_dashboard').url
        output_data = {
                            'logged_in':True,
                            'url':redirecturl
                        }
        return JsonResponse(output_data)



    else:
        form = allauthforms.LoginForm()
        allObject['form'] = form
        if request.GET.get('next'):
            allObject['next_page']=request.GET.get('next')
            allObject['redirect_url']=''.join(tuple(request.GET.get('next')))
        template_name = 'allauth/account/login.html'
        return render(request,template_name,allObject)
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'content':content,
                        }
        return JsonResponse(output_data)


def signup(request, *args, **kwargs):
    allObject = inherit(request,*args, **kwargs)
    if request.method == 'POST':
        chars = '0123456789' 
        token = ''
        for num in range(0,len(chars)):
            token = token +chars[round((random()-0.5)*len(chars))]
        token = token[0:6]
        user_id = 'D'+str(round(random()*123456789090929))
        user_id = user_id[0:10]
        # form.user_id = user_id
        chars = '0123456789' 
        token = ''
        for num in range(0,len(chars)):
            token = token +chars[round((random()-0.5)*len(chars))]
        token = token[0:6]                        
        erroroutput ="<ul class='text-danger p-0'>"
        errorlist = ''
        formerrors = []
        email =str(request.POST.copy().get('email')).lower()
        username = str(request.POST.copy().get('username')).lower()
        password = str(request.POST.copy().get('password'))
        first_name =str(request.POST.copy().get('first_name'))
        last_name= str(request.POST.copy().get('last_name'))
        harshed_password = make_password(password)
        if email:
            try:
                user = User.objects.get(email=email)
                formerrors.append('<li>Email already taken</li>')
            except ObjectDoesNotExist:
                try:
                    profile = pmodels.DpMembers.objects.get(email_addres=email)
                    formerrors.append('<li>Email already taken</li>')
                except ObjectDoesNotExist:
                    pass  
        if username:
            try:
                user = User.objects.get(username=username)
                formerrors.append('<li>Username already taken</li>')
            except ObjectDoesNotExist:
                pass  
        if len(formerrors) >0:
            erroroutput ="<ul class='text-danger p-0'>"
            errorlist = ''
            for error in formerrors:
                errorlist += '<li>' +str(error)+'</li>'
            erroroutput += errorlist + '</ul>'
            output_data = { 
                            'invalid':True,
                            'modal_notification':'<b>Ooops... Something is wrong!</b>' + erroroutput,
                            
                        }
            return JsonResponse(output_data)
        user = User.objects.create(password=harshed_password, username=username, 
        first_name =first_name,last_name= last_name, email= email or '')
        user.refresh_from_db()
        user.is_active = True
        user.save()
        # form.user_id = user_id
        exist = True
        while exist:
            nums = '0123456789'
            tempnums = ''
            lalph = 'abcdefghijklmnopqrstuvwxyz'
            templalph=''
            ualph = lalph.upper()
            tempualph = ''

            for num in range(0,len(nums)):
                tempnums +=nums[round((random()-0.5)*len(nums))]
            for num in range(0,len(lalph)):
                templalph +=lalph[round((random()-0.5)*len(lalph))]
            for num in range(0,len(ualph)):
                tempualph +=ualph[round((random()-0.5)*len(ualph))]
            firstletter= user.first_name[0].upper()
            lastletter =user.last_name[0].upper()
            temporary_userid = tempnums[0:3] + templalph[0:3]+tempualph[0:3]+firstletter+lastletter
            userid= []
            for char in temporary_userid:
                userid.insert(round(random()*5),char)
            userid = ''.join(userid)
            userid = 'D'+userid

            try:                
                pmodels.DpMembers.objects.get(member_no=userid)

            except ObjectDoesNotExist:
                pmodels.DpMembers.objects.create(user=user,userid=user_id,last_token=make_password(token),
                last_name=last_name,email_addres=email or '', first_name=first_name,member_no=userid)
                exist = False
                break
        if email:
            subject = 'Account Activation - Dominion Partners Global'
            message = render_to_string('allauth/account/email_confirm.html', {
                    'token': token,
                    'user':user,
                    'settings':allObject['settings'],
                    'request':request

                })
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [user.email, ]
            sendmail(recipient_list,message,message,subject)

            # try:
            #     send_mail( subject, message, email_from, recipient_list,html_message=message )
            # except socket.gaierror:
            #     pass
            subject = 'Login Details - DPG'
            current_site = Site.objects.get_current()
            message = render_to_string('allauth/account/default_password.html', {
                    'password': password,
                    'username': username,
                    'email':user.email,
                    'user':user
                })
            recipient_list = [user.email, ]
            sendmail(recipient_list,message,message,subject)

            # try:
            #     send_mail( subject, message, email_from, recipient_list,html_message=message )
            # except socket.gaierror:
            #     pass
        user.is_active = True
        user.save()
        login(request, user)
        allObject = inherit(request)
        if request.POST.copy().get('next'):
            redirectinstance= redirect(request.POST.copy().get('next'))
            redirecturl = redirectinstance.url
        else:
            if user.is_superuser:
                redirecturl = redirect('admin_dashboard').url
            else:
                redirecturl = redirect('partner_dashboard').url
        output_data = {
                            'logged_in':True,
                            'url':redirecturl
                        }
        return JsonResponse(output_data)
    else:
        form = gforms.SignUpForm()
        allObject = inherit(request, *args, **kwargs)
        allObject['form'] = form
        return render(request, 'allauth/account/signup.html', allObject)



def logoutuser(request, *args, **kwargs):
    auth.logout(request)
    form = allauthforms.LoginForm()
    allObject = inherit(request, *args, **kwargs)
    allObject['form'] = form
    template_name = 'allauth/account/login.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
                        'content':content,
                    }
    return redirect('account_login')


@login_required

def account_activation_sent(request,*args, **kwargs):
    template_name = 'allauth/account/verification_sent.html'
    return render(request,template_name)



@login_required
def activate(request,*args, **kwargs):
    if request.method=='POST':
        user = User.objects.get(username = request.user.username)
        activation_code = request.POST.copy().get('activation_code')
        try:
                partner = pmodels.DpMembers.objects.get(user=user,)
        except ObjectDoesNotExist:
                partner = pmodels.DpMembers.objects.get(user=user,)
        passwordcheck = check_password(str(activation_code),str(partner.last_token))

        if passwordcheck:
            partner.email_confirmed = True
            partner.last_token=''
            partner.save()

            output_data = {
                'modal_message':'Account successfully activated',
                        'activated':True,
                        'next_url':redirect('partner_dashboard').url
                        
                    }
            return JsonResponse(output_data)
        else:
            output_data = {
                        'invalid_code':True,
                    }
            return JsonResponse(output_data)






@login_required
def resendactivationcode(request,*args, **kwargs):
    allObject = inherit(request)
    chars = '0123456789'
    token = ''
    for num in range(0,len(chars)):
        token = token +chars[round((random()-0.5)*len(chars))]
    token = token[0:6] 
    user = request.user
    # user=User.objects.get(username = request.user.username)
    partner = pmodels.DpMembers.objects.get(user=user)
    partner.last_token=make_password(token)
    partner.save()
    subject = 'DPG - Activation Code'
    message = render_to_string('allauth/account/email_confirm.html', {
            'token':token,
            'user':user,
            'title':'ACCOUNT ACTIVATION',
            'request':request,
            'socials':gmodels.SocialLink.objects.all()
        })
    # message = render_to_string('padmin/happy_birthday.html', {
    #         'token':token,
    #         'user':user,
    #         'settings':allObject['settings'],
    #         'request':request,
    #         'title':'HAPPY BIRTHDAY!!!',
    #         'socials':gmodels.SocialLink.objects.all()
    #     })
    recipient_list = [user.email, ] 
    sendmail(recipient_list,message,message,subject)

    # try:
    #     send_mail( subject, message, email_from, recipient_list ,html_message=message ) 
    # except socket.gaierror:
    #     output_data = {
    #             'email_sent':True,
    #             'modal_notification':'Email send error',
    #                 }
    #     pass
    # except smtplib.SMTPConnectError:
    #     output_data = {
    #             'email_sent':True,
    #             'modal_notification':'Email send error',
    #                 }
    output_data = {
                    'email_sent':True,
                    'modal_notification':'your activation code has been resent to '+user.email,
                        }
    # output_data = {
    #         'email_sent':True,
    #         'modal_notification':token,
    #             }

    
    return JsonResponse(output_data)
