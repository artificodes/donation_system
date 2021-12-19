from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import query
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from general import forms as gforms
from django.core.exceptions import ObjectDoesNotExist
from general import models as gmodels
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
from partners.email_sender import sendmail
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponse, request
from django.views import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
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
from partners import models as pmodels
from partners import forms as pforms

import socket

allObject = {}



def inherit(request, *args, **kwargs):
    allObject ={}
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        current_user =[]
    else:
        current_user = pmodels.DpMembers.objects.get(user=user)
        try:
            settings = list(gmodels.General.objects.all())[0]
        except IndexError:
            settings =[]    
        allObject['settings'] = settings
        allObject['user'] = user
        allObject['homecardarticles'] = gmodels.CardArticle1.objects.all()
        allObject['server_timestamp'] = round(datetime.datetime.now().timestamp())
        allObject['socials'] = list(gmodels.SocialLink.objects.all())
        allObject['partner'] = current_user
        partner = allObject['partner']      
        allarticles = pmodels.Article.objects.all()
        events = pmodels.Event.objects.all()
        upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
        allObject['events']=upcomingevents
        articles = []
        notifications = []
        unreadnotificationscount = 0
        for event in events:
            notifications.append(event)
            if partner in event.read.all():
                pass
            else:
                unreadnotificationscount +=1    
        for article in allarticles:
            notifications.append(article)
            if partner in article.read.all():
                pass
            else:
                unreadnotificationscount +=1
        allannouncements = pmodels.Announcement.objects.all()
        announcements = []
        for announcement in allannouncements:
            notifications.append(announcement)
            if partner in announcement.read.all():
                pass
            else:
                unreadnotificationscount +=1
        supports = list(pmodels.Support.objects.filter(partner=partner))
        supports.sort(key=lambda x:x.date_time_added,reverse=True)
        for support in supports:
            if support.resolved:
                pass
            elif support.admin_resolved and not support.resolved:        
                notifications.append(support)
                unreadnotificationscount +=1    
        
        unreadnotifications = False
        if notifications:
            unreadnotifications = True
        notifications.sort(key=lambda x:x.date_time_added,reverse=True)
        allObject['notifications'] = notifications
        allObject['notificationscount'] = unreadnotificationscount

    return allObject




@login_required
def select_account_type(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =allObject['partner'] 
    allObject['title'] = 'DPG | Account selection'
    allObject['page'] = 'Account selection'
    allObject['next'] = request.GET.get('next') or '/'
    partnerstatus = checkpartnerstatus(request, partner)
    if partner.email_confirmed:
        pass
    elif not partner.email_confirmed and (partner.email_addres =='' or partner.email_addres =='none'):
        pass
    elif not partner.email_confirmed:
        return redirect('partner_confirm_email_page')
    else:
        pass
    # if partner.account_type_selected:
    #     if partner.profile_updated:
    #         pass
    #     else:
    #         return redirect('partner_update_profile')
    if request.method == 'POST':
        # if not partner.account_type == str(request.POST.copy().get('accounttype')):
        #     partner.photo = ''
        #     partner.profile_updated=False 
        partner.account_type=str(request.POST.copy().get('accounttype'))
        partner.account_type_selected=True

        partner.save()
        return redirect(redirect('partner_update_profile').url +'?next='+str(allObject['next'])) 

    template_name = 'partners/select_account_type.html'
    return render(request,template_name,allObject)




@login_required
def confirmemail(request,updated=False, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'partners/email_confirmation_form.html'
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  




@login_required
def confirmemailpage(request,updated=False, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    url = str(request.get_full_path())
    partner = allObject['partner']

    if partner.privacy_terms_accepted:
        pass
    else:
        return redirect(redirect('accept_privacy_terms').url +'?next='+url) 
    template_name = 'partners/email_confirmation_page.html'
    allObject['title'] = 'DPG | Confirm email'
    allObject['page'] = 'Account activation'
    allObject['next'] = request.GET.get('next')
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  



@login_required
def myprofile(request,updated=False, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'partners/profile.html'
    allObject['title'] ='DPG | Profile'
    allObject['page'] ='My Profile'
    content = loader.render_to_string(template_name,allObject,request)
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  


@login_required
def dashboardcontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        template_name = 'partners/dashboard_content.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'Due balance: ' + 'N2000',
                        }
        return JsonResponse(output_data)  
    else:
        output_data = {
        'modal_message':'Kindly update your profile',
                        }
        return JsonResponse(output_data)


@login_required
def informationdeskcontent(request,content=None,cid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        try:
            if str(content).lower() == 'article':
                reqcontent = pmodels.Article.objects.get(articleid=cid)
                
            elif str(content).lower() == 'announcement':
                reqcontent = pmodels.Announcement.objects.get(contentid=cid)
            elif str(content).lower() == 'event':
                reqcontent = pmodels.Event.objects.get(eventid=cid)
            reqcontent.read.add(partner)
            template_name = 'partners/information_desk_content.html'
            allObject['content']=reqcontent
            content = loader.render_to_string(template_name,allObject,request)
            output_data = {
                    'modal_content':content,
                    'heading':reqcontent.title,
                            }
            return JsonResponse(output_data) 
        except ObjectDoesNotExist:
            output_data = {
            'modal_message':'Content not found',
                    }
            return JsonResponse(output_data)   
         
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)


@login_required
def events(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    partnerstatus=checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
        try:
            todaysevent = pmodels.Event.objects.get(end_date_time__gt=datetime.datetime.now(),start_date_time__date=datetime.datetime.today().date())
            if todaysevent.start_date_time < datetime.datetime.now() and todaysevent.end_date_time > datetime.datetime.now():
                allObject['eventongoing'] =True         
        except ObjectDoesNotExist:
            todaysevent=''
            allObject['eventongoing'] =False
        upcomingevents.sort(key=lambda x: x.date_time_added,reverse=True)

        allObject['upcomingevents'] =upcomingevents
        pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
        pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['pastevents'] =pastevents
        allObject['title'] ='DPG | Events'
        allObject['page'] ='Events'
        allObject['todaysevent'] =todaysevent
        template_name = 'partners/events.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'Events',
                        }
        return render(request,template_name,allObject)
        return JsonResponse(output_data)  
    else:
        return partnerstatus


@login_required
def announcements(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    allObject['title'] ='DPG | Announcements'
    allObject['page'] ='Announcements'
    partnerstatus=checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        announcements =  list(pmodels.Announcement.objects.all())
        announcements.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['announcements'] =announcements
        template_name = 'partners/announcements.html' 
        return render(request,template_name,allObject)    
    else:
        return partnerstatus


@login_required
def support(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    allObject['title'] ='DPG | Support'
    allObject['page'] ='Support'
    partnerstatus=checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        supports=list(pmodels.Support.objects.filter(partner=partner,))
        supports.sort(key =lambda x:x.date_time_added,reverse=True)  
        allObject['supports'] = supports 
        template_name = 'partners/supports.html' 
        return render(request,template_name,allObject)    
    else:
        return partnerstatus



@login_required
def announcementdetails(request,announcementid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        announcement = pmodels.Announcement.objects.get(contentid=announcementid)
        announcement.read.add(partner)
        allObject['announcement'] = announcement
        template_name = 'partners/announcement_details.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'heading':announcement.title,
                'modal_content':content,
                        }
        return JsonResponse(output_data)  
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)



@login_required
def articles(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    allObject['title'] ='DPG | Articles'
    allObject['page'] ='Articles'
    partnerstatus=checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        articles =  list(pmodels.Article.objects.all())
        articles.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['articles'] =articles
        template_name = 'partners/articles.html' 
        return render(request,template_name,allObject)    
    else:
        return partnerstatus


@login_required
def articledetails(request,articleid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        article = pmodels.Article.objects.get(articleid=articleid)
        allObject['article'] = article
        template_name = 'partners/article_details.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'heading':article.title,
                'modal_content':content,
                        }
        return JsonResponse(output_data)  
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)




@login_required
def eventregistration(request,eventid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        event = pmodels.Event.objects.get(eventid=eventid)
        event.registrations.add(partner)
        event.save()
        upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
        upcomingevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['upcomingevents'] =upcomingevents
        pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
        pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['pastevents'] =pastevents
        template_name = 'partners/events.html'
        content = loader.render_to_string(template_name,allObject,request)
        template_name = 'general/success.html'
        allObject['message'] = 'Congratulations! You have successfully registered for ' + event.title
        message = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'Events',
                'message':message,
                'registered':True
                        }
        return JsonResponse(output_data)  
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)

from qr_code.qrcode.utils import QRCodeOptions
@login_required
def eventdetails(request,eventid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        event = pmodels.Event.objects.get(eventid=eventid)
        allObject['event'] = event
        input_data = str(event.eventid)
        template_name = 'partners/event_details.html'
        context = dict(
               qrc_options= QRCodeOptions(event.eventid,size='18', border=8, error_correction='L',image_format='png', ),
            )
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'modal_content':content,
                'heading':'Upcoming event',
                        }
        return JsonResponse(output_data)  
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)



@login_required
def supportdetails(request,supportid=None, *args, **kwargs):
    # allObject = inherit(request, *args, **kwargs)
    support = pmodels.Support.objects.get(supportid=supportid)
    allObject['support'] = support
    template_name = 'partners/support_details.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'modal_content':content,
            'heading':'Support',
                    }
    return JsonResponse(output_data)  
    


@login_required
def verifyevent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    if partner.profile_updated:
        try:
            event = pmodels.Event.objects.get(eventid=request.GET.get('eventid'))
            ongoingevents = list(pmodels.Event.objects.filter(end_date_time__gt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
            upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
            pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.datetime.now()))
            if event in ongoingevents:
                if partner in event.attendees.all():
                    message ='Your attendance has previously been recorded'
                    output_data = {
                        'message':message,
                        'attended':True
                                }
                    return JsonResponse(output_data)
                else:            
                    event.attendees.add(partner)
                    event.save()
                    template_name = 'general/success.html'
                    allObject['message'] = 'Congratulations, your attendance has been recorded'
                    successcontent = loader.render_to_string(template_name,allObject,request)
                    output_data = {
                        'message':successcontent,
                        'attended':True
                                }
                    return JsonResponse(output_data)
            else:
                output_data = {
                    'message':'Event is not available for attendance',
                    'past':True
                            }
                return JsonResponse(output_data)
  
        except ObjectDoesNotExist:
                output_data = {
                    'message':'Event not found',
                            }
                return JsonResponse(output_data)
    else:
        
        output_data = {
        'modal_message':'Kindly update your profile and try again',
                        }
        return JsonResponse(output_data)

import socket


@login_required
def changephoto(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    allObject['title']='DPG | Profile Update'
    allObject['page'] = 'Profile update'
    if request.method == 'POST':
        partner =allObject['partner']

        partnerinstance = pforms.changephoto(request.POST,request.FILES,instance=partner)
       
        if partnerinstance.is_valid():
            partnerinstance.save()
            template_name = 'general/success.html'
            message = 'Your profile picture was changed successfully'
            allObject['message'] = message
            successcontent = loader.render_to_string(template_name,allObject,request)
            allObject['message'] = message
            output_data = {
                'done':True,
                'modal_message':successcontent,
                            }        
                            
            return JsonResponse(output_data)
    else:
        partner =allObject['partner']

        template_name = 'partners/change_photo.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'modal_content':content,
                            'heading':'Change Profile Picture'
                        }
        # return render(request,template_name,allObject)
        return JsonResponse(output_data)    



@login_required
def updateprofile(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    allObject['title']='DPG | Profile Update'
    allObject['page'] = 'Profile update'
    if request.method == 'POST':
        partner =allObject['partner']
        if partner.account_type == 'I':
            # secretanswer = str(request.POST.copy().get('sqa'))
            # secretquestion =str(request.POST.copy().get('sq'))
            partnerinstance = pforms.updateindividualprofile(request.POST,request.FILES,instance=partner)
        elif partner.account_type == 'Cr':
            partnerinstance = pforms.updatecorporateprofile(request.POST,request.FILES,instance=partner)
        elif partner.account_type == 'S':
            partnerinstance = pforms.updatesponsorprofile(request.POST,request.FILES,instance=partner)

        elif partner.account_type == 'C':
            partnerinstance = pforms.updatecoupleprofile(request.POST,request.FILES,instance=partner)

        success_template_name = 'general/success.html'

        if partnerinstance.is_valid():
            partnerinstance.save()
            partnerinstance = partnerinstance.instance
            cgcc= str(request.POST.copy().get('cgcc'))
            if cgcc == 'yes':
                partner.is_cgcc_member = True
            else:
                partner.is_cgcc_member = False
            partner.save()
            partner.refresh_from_db()
            partner.first_name = str(request.POST.copy().get('first_name'))

            partner.last_name = str(request.POST.copy().get('last_name'))
            
            message = "Your profile has been successfully updated. If you didn't perform this action, kindly contact Dominion Partners to report this action. Thank you"
            partner.profile_updated = True
            partner.save()
            if str(request.POST.copy().get('email')) != request.user.email:
                partner.previous_email = request.user.email
                request.user.email=str(request.POST.copy().get('email'))
                partner.email_confirmed= False
                request.user.save()
                subject = 'Email Confirmation - Dominion Partners'
                current_site = Site.objects.get_current()
                chars = '0123456789' 
                token = ''
                for num in range(0,len(chars)):
                    token = token +chars[round((random()-0.5)*len(chars))]
                token = token[0:6] 
                partner.last_token=make_password(token)
                partner.save()
                message = render_to_string('allauth/account/email_confirm.html', {
                        'token': token,
                    })
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [request.user.email, ]
                try:
                    send_mail( subject, message, email_from, recipient_list )
                except socket.gaierror:
                    pass
                template_name = 'partners/email_confirmation_form.html'
                content = loader.render_to_string(template_name,allObject,request)
                message = 'Your profile was updated successfully'
                allObject['message'] = message
                successcontent = loader.render_to_string(success_template_name,allObject,request)
                allObject['message'] = message
                output_data = {
                    'heading':'Action Required',
                    'modal_content':content,
                                }        
                                
                return JsonResponse(output_data)
            profile_updated = True
            subject = 'Profile Updated'
            mail_body = 'Your profile  has been updated'
            message = render_to_string('partners/update_profile_email.html', {
                'message':mail_body,
                'user':request.user
                })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email, ] 
            # send_mail( subject, message, email_from, recipient_list ) 
            # content = loader.render_to_string(template_name,allObject,request)
            message = 'Your profile was updated successfully'
            allObject['message'] = message
            successcontent = loader.render_to_string(success_template_name,allObject,request)
            allObject['message'] = message
            output_data = {
                'done':True,
                # 'content':content,
                'next_url':request.POST.copy().get('next'),
                'modal_message':successcontent,
                            }        
                            
            return JsonResponse(output_data)
        output_data = {
            'done':True,
            'modal_message':partnerinstance.errors.as_text()

                        }  
        return JsonResponse(output_data)
            
    else:
        allObject['next'] = request.GET.get('next') or redirect('partner_my_profile').url

        partner =allObject['partner']
        # if partner.account_type=='I':
        #     template_name = 'partners/individual_profile_form.html'
        # elif partner.account_type=='Cr':
        #     template_name = 'partners/corporate_profile_form.html'
        # elif partner.account_type=='C':
        #     template_name = 'partners/couple_profile_form.html'
        # elif partner.account_type=='S':
        #     template_name = 'partners/sponsor_profile_form.html'           
        tvstations = list(pmodels.TvStation.objects.all())
        allObject['tvstations'] = tvstations
        template_name = 'partners/update_profile.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'modal_content':content,
                            'heading':'Update Profile'
                        }
        return render(request,template_name,allObject)

        return JsonResponse(output_data)    


def videos(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    videos = list(pmodels.Video.objects.all())
    videos.sort(key=lambda x: x.date_time_added,reverse=True)
    try:
        allObject['latestvideo'] = videos[0]
    except IndexError:
        pass
    allObject['videos'] =videos
    allObject['title']='DPG | Videos'
    allObject['page'] = 'Videos'
    template_name = 'partners/videos.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return render(request,template_name,allObject)

    return JsonResponse(output_data)

def monthlypayments(partner,allObject):
    monthlypayments = []
    for payment in readypayments:
        for monthpayment in payment.months.all():
            monthlypayments.append(monthpayment)      
    monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)

    lastmonthpayments = filter(lambda x:x.month_covered.month == datetime.datetime.today().month-1 and x.month_covered.year == datetime.datetime.today().year,monthlypayments)
    thismonthpayments = filter(lambda x:x.month_covered.month == datetime.datetime.today().month and x.month_covered.year == datetime.datetime.today().year,monthlypayments)
    thismonthpaymentsamount = 0
    for payment in thismonthpayments:
        thismonthpaymentsamount+=payment.amount
    lastmonthpaymentsamount = 0
    for payment in lastmonthpayments:
        lastmonthpaymentsamount+=payment.amount
    if thismonthpaymentsamount ==0:
        monthpercentageincrease =0
    else:
        monthpercentageincrease = round((thismonthpaymentsamount -lastmonthpaymentsamount)/thismonthpaymentsamount *100)
    lastyearpayments = filter(lambda x:x.month_covered.year == datetime.datetime.today().year-1,monthlypayments)
    thisyearpayments = filter(lambda x:x.month_covered.year == datetime.datetime.today().year,monthlypayments)
    thisyearpaymentsamount = 0
    for payment in thisyearpayments:
        thisyearpaymentsamount+=payment.amount
    lastyearpaymentsamount = 0
    for payment in lastyearpayments:
        lastyearpaymentsamount+=payment.amount
    if thisyearpaymentsamount ==0:
        yearpercentageincrease =0
    else:
        yearpercentageincrease = round((thisyearpaymentsamount -lastyearpaymentsamount)/thisyearpaymentsamount *100)
    pendingupdate =  list(filter(lambda x:x.updated==False,payments))
    pendingapproval =  list(filter(lambda x: x.approved==False,payments))
    page = 1

    paginator = Paginator(monthlypayments, 5)
    try:
        monthlypayments = paginator.page(page)
    except PageNotAnInteger:
        monthlypayments = paginator.page(1)
    except EmptyPage:
        monthlypayments = paginator.page(paginator.num_pages)
    allObject['monthlypayments'] = monthlypayments
    allObject['monthpercentageincrease'] = monthpercentageincrease
    allObject['thismonthpaymentsamount'] ='{:,.2f}'.format(thismonthpaymentsamount)
    allObject['yearpercentageincrease'] = yearpercentageincrease
    allObject['thisyearpaymentsamount'] ='{:,.2f}'.format(thisyearpaymentsamount)


def regularizepayments(request,*args, **kwargs):
    allObject = inherit(request,*args, **kwargs )
    partners = pmodels.DpMembers.objects.all()
    for partner in partners:
        if not partner.payment_synced:
            otherpayments = list(pmodels.DpPayments.objects.filter(member_no=partner.member_no))
            months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
            other_payments_obj_by_year ={}
            for payment in otherpayments:
                payment.month_covered=str(payment.payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
                payment.save()
                try:
                    yearpayments = other_payments_obj_by_year[payment.payment_year]
                    yearpayments.append(payment)
                except KeyError:
                    other_payments_obj_by_year[payment.payment_year] = []
                    yearpayments = other_payments_obj_by_year[payment.payment_year]
                    yearpayments.append(payment)
            for year,yearspaymentslist in other_payments_obj_by_year.items():
                for payment in yearspaymentslist:
                    try:
                        batchpayment = pmodels.Payment.objects.get(partner=partner, start_date__lt=datetime.datetime.now(),start_date__year=int(year),
                        end_date__lt =datetime.datetime.now(),end_date__year=int(year))
                    except ObjectDoesNotExist:
                        batchpayment = pmodels.Payment.objects.create(partner=partner, approved=True,currency=payment.currency,
                        start_date=str(yearspaymentslist[0].payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
                        ,end_date=str(yearspaymentslist[len(yearspaymentslist)-1].payment_year)+'-'+str(months.index(yearspaymentslist[len(yearspaymentslist)-1].payment_month)+1)+'-'+'1')
                    batchpayment.refresh_from_db()
                    if payment in batchpayment.months.all():
                        pass
                    else:
                        batchpayment.months.add(payment)

                    batchpayment.amount+=payment.amount
                    batchpayment.updated=True
                    batchpayment.save()
            partner.payment_synced = True
            partner.save()

    output_data = { 
                    'content':'Done',
                    # 'next_page':monthlypayments.next_page_number()
                    
                }
    return JsonResponse(output_data)




# @login_required
def allpayments(request,userid=None,*args, **kwargs):
    allObject = inherit(request,*args, **kwargs )
    partner = pmodels.DpMembers.objects.get(member_no=userid)
    if not partner.payment_synced:
        otherpayments = list(pmodels.DpPayments.objects.filter(member_no=partner.member_no))
        months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        other_payments_obj_by_year ={}
        for payment in otherpayments:
            payment.month_covered=str(payment.payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
            payment.save()
            try:
                yearpayments = other_payments_obj_by_year[payment.payment_year]
                yearpayments.append(payment)
            except KeyError:
                other_payments_obj_by_year[payment.payment_year] = []
                yearpayments = other_payments_obj_by_year[payment.payment_year]
                yearpayments.append(payment)
        for year,yearspaymentslist in other_payments_obj_by_year.items():
            for payment in yearspaymentslist:
                try:
                    batchpayment = pmodels.Payment.objects.get(partner=partner, start_date__lt=datetime.datetime.now(),start_date__year=int(year),
                    end_date__lt =datetime.datetime.now(),end_date__year=int(year))
                except ObjectDoesNotExist:
                    batchpayment = pmodels.Payment.objects.create(partner=partner, approved=True,currency=payment.currency,
                    start_date=str(yearspaymentslist[0].payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
                    ,end_date=str(yearspaymentslist[len(yearspaymentslist)-1].payment_year)+'-'+str(months.index(yearspaymentslist[len(yearspaymentslist)-1].payment_month)+1)+'-'+'1')
                batchpayment.refresh_from_db()
                if payment in batchpayment.months.all():
                    pass
                else:
                    batchpayment.months.add(payment)

                batchpayment.amount+=payment.amount
                batchpayment.updated=True
                batchpayment.save()
        partner.payment_synced = True
        partner.save()
    # otherpayments = list(pmodels.DpPayments.objects.filter(partner=partner))
    # otherpayments.sort(key =lambda x:x.date_time_added,reverse=True)
    payments=list(pmodels.Payment.objects.filter(partner=partner,deleted=False))
    payments.sort(key =lambda x:x.end_date,reverse=True)
    readypayments = list(filter(lambda x:x.updated==True and x.approved==True,payments))
    pendingupdate =  list(filter(lambda x:x.updated==False,payments))
    pendingapproval =  list(filter(lambda x: x.approved==False,payments))
    page = 1

    paginator = Paginator(readypayments, 7)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    allObject['pendingupdates'] = pendingupdate
    allObject['pendingapprovals'] = pendingapproval
    allObject['payments'] = payments
    try:
        if allObject['admin'].is_superuser:
            monthlypayments = []
            for payment in readypayments:
                for monthpayment in payment.months.all():
                    monthlypayments.append(monthpayment)      
            monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)

            lastmonthpayments = filter(lambda x:x.month_covered.month == datetime.datetime.today().month-1 and x.month_covered.year == datetime.datetime.today().year,monthlypayments)
            thismonthpayments = filter(lambda x:x.month_covered.month == datetime.datetime.today().month and x.month_covered.year == datetime.datetime.today().year,monthlypayments)
            thismonthpaymentsamount = 0
            for payment in thismonthpayments:
                thismonthpaymentsamount+=payment.amount
            lastmonthpaymentsamount = 0
            for payment in lastmonthpayments:
                lastmonthpaymentsamount+=payment.amount
            if thismonthpaymentsamount ==0:
                monthpercentageincrease =0
            else:
                monthpercentageincrease = round((thismonthpaymentsamount -lastmonthpaymentsamount)/thismonthpaymentsamount *100)
            lastyearpayments = filter(lambda x:x.month_covered.year == datetime.datetime.today().year-1,monthlypayments)
            thisyearpayments = filter(lambda x:x.month_covered.year == datetime.datetime.today().year,monthlypayments)
            thisyearpaymentsamount = 0
            for payment in thisyearpayments:
                thisyearpaymentsamount+=payment.amount
            lastyearpaymentsamount = 0
            for payment in lastyearpayments:
                lastyearpaymentsamount+=payment.amount
            if thisyearpaymentsamount ==0:
                yearpercentageincrease =0
            else:
                yearpercentageincrease = round((thisyearpaymentsamount -lastyearpaymentsamount)/thisyearpaymentsamount *100)
            pendingupdate =  list(filter(lambda x:x.updated==False,payments))
            pendingapproval =  list(filter(lambda x: x.approved==False,payments))
            page = 1

            paginator = Paginator(monthlypayments, 5)
            try:
                monthlypayments = paginator.page(page)
            except PageNotAnInteger:
                monthlypayments = paginator.page(1)
            except EmptyPage:
                monthlypayments = paginator.page(paginator.num_pages)
            allObject['monthlypayments'] = monthlypayments
            allObject['monthpercentageincrease'] = monthpercentageincrease
            allObject['thismonthpaymentsamount'] ='{:,.2f}'.format(thismonthpaymentsamount)
            allObject['yearpercentageincrease'] = yearpercentageincrease
            allObject['thisyearpaymentsamount'] ='{:,.2f}'.format(thisyearpaymentsamount)        

    except Exception:
        pass 
    allObject['partner'] = partner
    template_name = 'partners/payments.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = { 
                    'content':content,
                    # 'next_page':monthlypayments.next_page_number()
                    
                }
    return JsonResponse(output_data)



def checkpartnerstatus(request, partner):
    url = str(request.get_full_path())
    if partner.privacy_terms_accepted:
        pass
    else:
        return redirect(redirect('accept_privacy_terms').url +'?next='+url) 

    if partner.email_confirmed:
        pass
    elif not partner.email_confirmed and (partner.email_addres =='' or partner.email_addres =='none'):
        pass
    elif not partner.email_confirmed:
        return redirect(redirect('partner_confirm_email_page').url +'?next='+url)
    else:
        pass
    if partner.account_type_selected:
        if partner.profile_updated:
            pass
        else:
            return redirect(redirect('partner_update_profile').url +'?next='+url) 
    else:
        return  redirect(redirect('partner_select_account_type').url +'?next='+url)

    return True


@login_required
def dashboard(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'partners/dashboard.html'
    partner = allObject['partner']
    allObject['title']='DPG | Dashboard'
    allObject['page'] = 'Dashboard'
    partnerstatus = checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        
        return render(request,template_name,allObject)

    else:
        return partnerstatus


def recentremittances(request,userid=None,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = pmodels.DpMembers.objects.get(member_no=userid)
    payments=list(pmodels.Payment.objects.filter(partner=partner))
    payments.sort(key =lambda x:x.date_time_added,reverse=True)
    readypayments = list(filter(lambda x:x.updated==True and x.approved==True,payments))
    pendingupdate =  list(filter(lambda x:x.updated==False,payments))
    pendingapproval =  list(filter(lambda x: x.approved==False,payments))
    page = request.GET.get('page', 2)

    paginator = Paginator(readypayments, 2)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    allObject['pendingupdates'] = pendingupdate
    allObject['pendingapprovals'] = pendingapproval
    allObject['payments'] = payments
    template_name = 'partners/recent_remittances.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = { 
                    'content':content,
                   'next_page':payments.has_next()
                    
                }
    return JsonResponse(output_data)

@login_required
def mypayments(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner = allObject['partner']
    allObject['title'] = 'DPG | My Payments'
    allObject['partner'] = partner
    allObject['page'] = 'My Payments'
    partnerstatus=checkpartnerstatus(request, partner)
    if type(partnerstatus) == bool:
        # allpayments(request,partner,allObject)
        template_name = 'partners/my_payments.html'  
        return render(request,template_name,allObject)
    else:
        return partnerstatus
    




@login_required
def updatepayment(request,paymentid=None, *args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']
    payment = pmodels.Payment.objects.get(paymentid=paymentid,partner=partner)
    if request.method == 'POST':
        # parent_thumbnail = str(request.POST.copy().get('parent_thumbnail'))
        # day = uforms.addeventday(request.POST,request.FILES)
        end_date_time_str = str(request.POST.copy().get('end_date_time'))
        end_date_time_obj = datetime.datetime.strptime(end_date_time_str, '%m/%d/%Y %I:%M %p')
        start_date_time_str = str(request.POST.copy().get('start_date_time'))
        start_date_time_obj = datetime.datetime.strptime(start_date_time_str, '%m/%d/%Y %I:%M %p')
        amount = int(request.POST.copy().get('amount'))
        payment = pmodels.Payment.objects.filter(paymentid=paymentid,partner=partner).update(end_date_time=end_date_time_obj,
        start_date_time=start_date_time_obj,)
        payment=pmodels.Payment.objects.get(paymentid=paymentid)
        periodcounter = end_date_time_obj.month - start_date_time_obj.month
        counter = 0
        monthlyamount = amount/(periodcounter+1)
        for month in range(1,periodcounter+2):
            if counter == 0:
                coveredmonth = pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,amount=monthlyamount,month_covered=start_date_time_obj,paymentid=payment.paymentid,partner=partner)
                counter +=1
                payment.months.add(coveredmonth)
            elif month-1 + start_date_time_obj.month == end_date_time_obj.month:
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,amount=monthlyamount,paymentid=payment.paymentid,partner=partner)
                year = str(start_date_time_obj.year)
                month = str(start_date_time_obj.month +month-1)
                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.member_no=partner.member_no
                coveredmonth.save()
                payment.months.add(coveredmonth)
                break
            else:
                # dateobject = datetime.datetime.date()
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,amount=monthlyamount,paymentid=payment.paymentid,partner=partner)
                year = str(start_date_time_obj.year)
                month = str(start_date_time_obj.month + month-1)
                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.member_no=partner.member_no
                coveredmonth.save()
                payment.months.add(coveredmonth)
        payment.updated=True
        payment.save()
        payment.refresh_from_db()
        payment_details_template = 'partners/payments.html'
        payment_details = loader.render_to_string(payment_details_template,allObject,request)
        output_data = { 
                        'done':True,
                        'message':'Payment updated',
                        'content':payment_details,
                        'exit':True
                        
                    }
        return JsonResponse(output_data)
    else:
        allObject['payment']=payment
        template_name = 'partners/update_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Update Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)

@login_required
def cancelpayment(request,paymentid=None, *args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']
    payment = pmodels.Payment.objects.get(paymentid=paymentid,partner=partner)
    if request.method == 'POST':

        payment.deleted = True
        payment.save()
        payments=list(pmodels.Payment.objects.filter(partner=partner,deleted=False,approved=False))
        payments.sort(key =lambda x:x.date_time_added,reverse=True)
        allObject['pendingapprovals'] = payments
        payment_details_template = 'partners/pending_payments.html'
        payment_details = loader.render_to_string(payment_details_template,allObject,request)
        output_data = { 
                        'content':payment_details,
                        'exit':True
                        
                    }
        return JsonResponse(output_data)
    else:
        allObject['payment']=payment
        template_name = 'partners/update_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'message':'Are you sure you want to cancel this payment?',
                        'removeurl':redirect('partner_cancel_payment',paymentid=paymentid).url,
                        
                    }
        return JsonResponse(output_data)




def updatecurrentpayment(request, payment,partner):
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    currentmonth=payment.start_date.month
    currentyear=payment.start_date.year
    if (payment.end_date.year < payment.start_date.year) or ((payment.end_date.month < payment.start_date.month) and payment.end_date.year == payment.start_date.year ):
        payment.delete()
        output_data = { 
                    'done':False,
                    'message':'Invalid dates supplied',                            
                }
        return JsonResponse(output_data)
    period = request.POST.copy().get('period')
    if period == 'custom':
        while currentmonth < 13:
            if currentmonth ==12:
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,paymentid=payment.paymentid,partner=partner)
                year = str(currentyear)
                month = str(currentmonth)

                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.payment_month = months[int(month)-1]
                coveredmonth.payment_year = year                 
                coveredmonth.member_no=partner.member_no
                coveredmonth.save()
                payment.months.add(coveredmonth)
                message='entered first loop'
                if payment.end_date.year == currentyear and payment.end_date.month == currentmonth:
                    break
                else:
                    currentyear +=1                    
                # if payment.end_date.year != currentyear:
                currentmonth =1


            else:
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,paymentid=payment.paymentid,partner=partner)
                year = str(currentyear)
                month = str(currentmonth)

                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.payment_month = months[int(month)-1]
                coveredmonth.payment_year = year                
                coveredmonth.member_no=partner.member_no
                coveredmonth.save()
                payment.months.add(coveredmonth)
                message='never entered first loop'
                if payment.end_date.year == currentyear and payment.end_date.month == currentmonth:
                    break
                currentmonth +=1
        monthsamount =payment.amount/payment.months.count()
    
    elif period == 'current':
        partnerplan = partner.contribution_frequency
        if partnerplan == 'yearly':
            payment.start_date=str(datetime.datetime.now().year)+'-1'+'-1'
            payment.end_date=str(datetime.datetime.now().year)+'-12'+'-1'
            monthsamount =payment.amount/12
            for month in range(1,13):

                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,paymentid=payment.paymentid,partner=partner)
                year = str(datetime.datetime.now().year)
                month = str(month)
             
                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.payment_month = months[int(month)-1]
                coveredmonth.payment_year = year                  
                coveredmonth.member_no=partner.member_no
                coveredmonth.save()
                payment.months.add(coveredmonth)
        elif partnerplan == 'monthly':
            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().month)
            day = str(1)            
            payment.start_date=year+'-'+month+'-'+day
            payment.end_date=year+'-'+month+'-'+day
            monthsamount =payment.amount
            coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,paymentid=payment.paymentid,partner=partner)

            coveredmonth.refresh_from_db()
            coveredmonth.member_no=partner.member_no
            coveredmonth.payment_month = months[int(month)-1]
            coveredmonth.payment_year = year
            coveredmonth.save()
            payment.months.add(coveredmonth)
        elif partnerplan == 'quarterly':
            quarters = [[1,2,3,4], [5,6,7,8],[9,10,11,12]]
            currentmonth = datetime.datetime.now().month
            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().month)
            day = str(1)  
            monthsamount =payment.amount/4
            for quarter in quarters:
                if currentmonth in quarter:
                    payment.start_date=year+'-'+str(quarter[0])+'-'+day
                    payment.end_date=year+'-'+str(quarter[len(quarter)-1])+'-'+day
                    for month in quarter:
                        coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,currency=payment.currency,paymentid=payment.paymentid,partner=partner)
                        year = str(datetime.datetime.now().year)
                        month = str(month)
                        day = str(1)
                        coveredmonth.refresh_from_db()
                        coveredmonth.payment_month = months[int(month)-1]
                        coveredmonth.payment_year = year
                        coveredmonth.member_no=partner.member_no
                        coveredmonth.save()
                        payment.months.add(coveredmonth)           
                    break 




    for monthlypayment in payment.months.all():
        monthlypayment.amount = monthsamount
        monthlypayment.save()

    
    payment.updated=True
    payment.save()
    payment.refresh_from_db()
    return True


@login_required
def createpayment(request,action=None, *args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']

    if request.method == 'POST':
        payment = pforms.createpayment(request.POST)
        if payment.is_valid:
            payment.save(commit=False)
            payment=payment.instance
            payment.DpMembers = partner
            payment.save()
            updatecurrentpayment(request,payment)
            allpayments(partner)

            if action == 'next':
                template_name = 'partners/create_payment.html'
                content = loader.render_to_string(template_name,allObject,request)
                payment_details_template = 'partners/payments.html'
                payment_details = loader.render_to_string(payment_details_template,allObject,request)
                output_data = { 
                                'done':True,
                                'message':'Payment added',
                                'modal_content':content,
                                'content':payment_details,
                                'next':True
                                
                            }
                return JsonResponse(output_data)
            elif action =='exit':
                payment_details_template = 'partners/payments.html'
                payment_details = loader.render_to_string(payment_details_template,allObject,request)
                output_data = { 
                                'done':True,
                                'message':'Payment added',
                                'content':payment_details,
                                'exit':True
                                
                            }
                return JsonResponse(output_data)
    else:
           
        template_name = 'partners/create_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Create Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)


@login_required
def changesupportstatus(request,supportid=None,status=None,*args, **kwargs):
    allObject = inherit(request)
    support = pmodels.Support.objects.get(supportid=supportid)
    if status == 'resolved':
        support.admin_resolved=True
        support.partner_resolved=True
        support.resolved=True    
        allObject['message'] = "Support has been marked as <span class='text-darker h3'>" + str(str(status).capitalize()) +"</span>"
        success_template = 'general/success.html'
        message = loader.render_to_string(success_template,allObject,request)
    elif status == 'unresolved':
        support.admin_resolved=True
        support.partner_resolved=False
        support.resolved=False
        message = "Support has been marked as <span class='text-darker h3'>" + str(str(status).capitalize()) +".</span> <br>Kindly give some time for an admin to respond. Thank you"
    support.save()
    allObject['support'] = support          
    output_data = { 
                    'modal_message':message,
                }
    return JsonResponse(output_data)


@login_required
def createsupport(request,*args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']

    if request.method == 'POST':
        support = pforms.createsupport(request.POST)
        if support.is_valid:
            support.save(commit=False)
            support=support.instance
            support.partner = partner
            support.save()
            support.refresh_from_db()
            allObject['support'] = support          
            template_name = 'partners/support.html'
            support = loader.render_to_string(template_name,allObject,request)
            success_template = 'general/success.html'
            allObject['message'] = 'Support sent successfully'
            message = loader.render_to_string(success_template,allObject,request)
            output_data = { 
                            'modal_message':message,
                            'content':support,                            
                        }
            return JsonResponse(output_data)

    else:
           
        template_name = 'partners/create_support.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Add Support',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)

@login_required
def recordpayment(request,*args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']
    paymentid = request.GET.get('tx_ref')
    referenceid = request.GET.get('transaction_id')
    status = request.GET.get('status')
    payment = pmodels.Payment.objects.get(paymentid=paymentid,partner=partner)
    payment.referenceid = referenceid
    payment.status = status
    if status =='successful':
        payment.approved = True

    payment.save()
    return redirect('partner_my_payments')
    output_data = { 
                    'done':True,
                    'modal_notification':'Payment approved',
                    
                }
    return JsonResponse(output_data)

def fixdb(request,*args, **kwargs):
    payments = list(pmodels.DpPayments.objects.all())
    counter = 1
    def savepayment(payment,counter):
        print(payment.pk)
        payment.fixed = True
        payment.save()

    [savepayment(payment,counter) for payment in payments if payment.fixed==False]

    # for payment in payments:
    #     print(counter)
    #     payment.save()
    #     counter+=1
    return redirect('partner_dashboard')
    output_data = { 
                    'done':True,
                    'modal_notification':'Payment approved',
                    
                }
    return JsonResponse(output_data)

@login_required
def makepayment(request,userid=None, *args, **kwargs):
    allObject = inherit(request)
    partner = allObject['partner']
    if request.method == 'POST':
        try:
            currencyid = int(request.POST.copy().get('currency'))
            currency = pmodels.Currency.objects.get(pk=currencyid)      
        except ObjectDoesNotExist:
            output_data = { 
                            'modal_message':'Invalid currency',                      
                        }
            return JsonResponse(output_data)   
        payment = pforms.makepayment(request.POST)
        if payment.is_valid:
            payment.save(commit=False)
            payment=payment.instance
            payment.partner = partner
            payment.currency = currency.symbol
            payment.save()
            updatecurrentpayment(request,payment,partner)        
            output_data = { 
                            'pay':True,
                            'amount':payment.amount,  
                            'paymentid':payment.paymentid,                          
                            'currency':payment.currency,
                            'key':str(currency.key)                    
                        }
            return JsonResponse(output_data)
    else:
        currencies = pmodels.Currency.objects.all()
        allObject['currencies']=currencies
        template_name = 'partners/make_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Make Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)


@login_required
def getcurrencykey(request, *args, **kwargs):
    allObject = inherit(request)
    if request.method == 'POST':
        try:
            symbol = str(request.POST.copy().get('symbol'))
            currency = pmodels.Currency.objects.get(symbol=symbol)      
        except ObjectDoesNotExist:
            output_data = { 
                            'modal_message':'Invalid currency',                      
                        }
            return JsonResponse(output_data)       
        output_data = { 
                        'key':str(currency.key)                    
                    }
        return JsonResponse(output_data)

