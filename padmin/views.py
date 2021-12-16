from typing import Type
from general.views import membersignup
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
from random import random
from excel_response import ExcelResponse
import xlwt
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
import partners
import pdfkit
from django.template import loader
import os
import base64
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from wkhtmltopdf.views import PDFTemplateView
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
from partners import forms as pforms
import django_excel as excel

allObject = {}


def inherit(request, *args, **kwargs):
    allObject={}
    if request.user.is_authenticated:
        admin = User.objects.get(username=request.user.username,is_superuser=True)
        allObject['admin'] = admin
    try:
        settings = list(gmodels.General.objects.all())[0]
    except IndexError:
        settings =[]
    allObject['settings'] = settings
    allObject['homecardarticles'] = gmodels.CardArticle1.objects.all()
    allObject['server_timestamp'] = round(datetime.datetime.now().timestamp())
    supports = list(pmodels.Support.objects.all())
    supports.sort(key=lambda x:x.date_time_added,reverse=True)
    notifications = []
    unreadnotificationscount = 0
    for support in supports:
        if support.resolved:
            pass
        elif (support.admin_resolved and not support.partner_resolved) or not support.admin_resolved:        
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
def informationdeskcontent(request,content=None,cid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    try:
        if str(content).lower() == 'article':
            reqcontent = pmodels.Article.objects.get(articleid=cid)
            
        elif str(content).lower() == 'announcement':
            reqcontent = pmodels.Announcement.objects.get(contentid=cid)
        elif str(content).lower() == 'event':
            reqcontent = pmodels.Event.objects.get(eventid=cid)
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
        return updateprofileform(request, *args, **kwargs)



@login_required
def supports(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    allObject['title'] ='DPG | Support'
    allObject['page'] ='Support'
    supports =  list(pmodels.Support.objects.all())
    supports.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['supports'] =supports
    template_name = 'padmin/supports.html' 
    return render(request,template_name,allObject)    


@login_required
def replysupport(request,supportid=None,*args, **kwargs):
    allObject = inherit(request)
    if request.method == 'POST':
        support = pmodels.Support.objects.get(supportid=supportid)
        support = pforms.createsupport(request.POST,instance=support)
        if support.is_valid:
            support.save()
            support = support.instance
            support.admin_resolved=True
            support.partner_resolved=True
            support.save()
            allObject['support'] = support          
            success_template = 'general/success.html'
            allObject['message'] = 'Support replied successfully. Partner will be notified'
            message = loader.render_to_string(success_template,allObject,request)
            output_data = { 
                            'modal_message':message,
                        }
            return JsonResponse(output_data)

def loginuser(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    # if request.user.is_authenticated:
    #     logout(request)
    #     return redirect('account_login')

    if request.method == 'POST':
    #form =allauthforms.LoginForm(request.POST)
    #if form.is_valid():
        username = request.POST.copy().get('login')
        raw_password = request.POST.copy().get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=raw_password)
        except ObjectDoesNotExist:
            admin = User.objects.get(email=username)
            admin = authenticate(username=user.username, password=raw_password)
        if user.is_superuser:             
            login(request, user)   
            admin = True
            allObject = inherit(request)
            # admin = User.objects.get(user=user)
            template_name = 'padmin/dashboard.html'
            content = loader.render_to_string(template_name,allObject,request)
            if request.POST.copy().get('next'):
                    redirectinstance= redirect(request.POST.copy().get('next'))
            output_data = {
                                'logged_in':True,
                                'url':redirectinstance.url
                            }
            return JsonResponse(output_data)
            output_data = {
                                'content':content,
                            }
            return redirect('dashboard')
        else:
            form = allauthforms.LoginForm()
            allObject['form'] = form
            template_name = 'allauth/account/login.html'
            return render(request,template_name,allObject)
            # return JsonResponse(output_data)
        # except ObjectDoesNotExist:
        #     admin = pmodels.DpMembers.objects.get(user=user)
        #     admin=True 
        #     output_data = {
        #         'logged_in':True,
        #         'partner':partner
        #                     }
        #     return cviews.home(request, *args, **kwargs)


    else:
        form = allauthforms.LoginForm()
        allObject['form'] = form
        if request.GET.get('next'):
            allObject['next_page']=request.GET.get('next')
            allObject['redirect_url']=''.join(tuple(request.GET.get('next')))
        template_name = 'allauth/account/login.html'
        return render(request,template_name,allObject)


@login_required
def allpayments(request,*args, **kwargs):
    allObject = inherit(request,*args, **kwargs )
    # partners = pmodels.DpMembers.objects.filter(del_flg='N')
    # for partner in partners:
    #     if not partner.payment_synced:
    #         otherpayments = list(pmodels.DpPayments.objects.filter(member_no=partner.member_no))
    #         months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    #         other_payments_obj_by_year ={}
    #         for payment in otherpayments:
    #             payment.month_covered=str(payment.payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
    #             payment.save()
    #             try:
    #                 yearpayments = other_payments_obj_by_year[payment.payment_year]
    #                 yearpayments.append(payment)
    #             except KeyError:
    #                 other_payments_obj_by_year[payment.payment_year] = []
    #                 yearpayments = other_payments_obj_by_year[payment.payment_year]
    #                 yearpayments.append(payment)
    #         for year,yearspaymentslist in other_payments_obj_by_year.items():
    #             for payment in yearspaymentslist:
    #                 try:
    #                     batchpayment = pmodels.Payment.objects.get(partner=partner, start_date__lt=datetime.datetime.now(),start_date__year=int(year),
    #                     end_date__lt =datetime.datetime.now(),end_date__year=int(year))
    #                 except ObjectDoesNotExist:
    #                     batchpayment = pmodels.Payment.objects.create(partner=partner, approved=True,currency=payment.currency,
    #                     start_date=str(yearspaymentslist[0].payment_year)+'-'+str(months.index(payment.payment_month)+1)+'-'+'1'
    #                     ,end_date=str(yearspaymentslist[len(yearspaymentslist)-1].payment_year)+'-'+str(months.index(yearspaymentslist[len(yearspaymentslist)-1].payment_month)+1)+'-'+'1')
    #                 batchpayment.refresh_from_db()
    #                 if payment in batchpayment.months.all():
    #                     pass
    #                 else:
    #                     batchpayment.months.add(payment)
    #                 # try:
    #                 #     coveredmonth = pmodels.MonthlyPayment.objects.get(partner=partner,amount=payment.amount, payment_year=payment.payment_year,payment_month=payment.payment_month)
    #                 # except ObjectDoesNotExist:
    #                 #     coveredmonth =pmodels.MonthlyPayment.objects.create(currency=payment.currency,partner=partner,amount=payment.amount,
    #                 #     payment_year=payment.payment_year,payment_month=payment.payment_month,)
    #                 #     year = str(payment.payment_year)
    #                 #     month = str(months.index(payment.payment_month)+1)
    #                 #     day = str(1)
    #                 #     coveredmonth.refresh_from_db()
    #                 #     # coveredmonth.payment_month = months[int(month)-1]year+'-'+month+'-'+day
    #                 #     # coveredmonth.payment_year = year                 datetime.datetime(int(payment.payment_year),months.index(payment.payment_month)+1,1)
    #                 #     coveredmonth.month_covered=year+'-'+month+'-'+day
    #                 #     coveredmonth.created_on = payment.created_on
    #                 #     coveredmonth.date_time_added=payment.created_on
    #                 #     coveredmonth.save()
    #                 #     batchpayment.months.add(coveredmonth)
    #                 batchpayment.amount+=payment.amount
    #                 batchpayment.updated=True
    #                 batchpayment.save()
    #         partner.payment_synced = True
    #         partner.save()
    #     other_payments_obj_by_year ={}

    payments = list(pmodels.Payment.objects.all())
    payments.sort(key =lambda x:x.end_date,reverse=True)
    readypayments = list(filter(lambda x:x.updated==True and x.approved==True,payments))
    pendingupdate =  list(filter(lambda x:x.updated==False,payments))
    pendingapproval =  list(filter(lambda x: x.approved==False,payments))
    page = 1

    paginator = Paginator(readypayments, 5)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    allObject['pendingupdates'] = pendingupdate
    allObject['pendingapprovals'] = pendingapproval
    allObject['payments'] = payments      

    # allObject['partner'] = partner
    template_name = 'padmin/payments.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = { 
                    'content':content,
                    # 'next_page':monthlypayments.next_page_number()
                    
                }
    return JsonResponse(output_data)



def members_payment_analysis(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    if userid == 'all':
        recentpayments = list(pmodels.Payment.objects.filter(approved=True))
        monthlypayments = list(pmodels.DpPayments.objects.all())
        # for payment in recentpayments:
        #     payment.delete()
    else:
        recentpayments = list(pmodels.Payment.objects.filter(partner__member_no=userid,approved=True))
        monthlypayments=[]
        for payment in recentpayments:
            for monthpayment in payment.months.all():
                monthlypayments.append(monthpayment)    
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
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

    allObject['monthpercentageincrease'] = monthpercentageincrease
    allObject['thismonthpaymentsamount'] ='{:,.2f}'.format(thismonthpaymentsamount)
    allObject['yearpercentageincrease'] = yearpercentageincrease
    allObject['thisyearpaymentsamount'] ='{:,.2f}'.format(thisyearpaymentsamount)
    template_name = 'padmin/payments_analysis.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)



def members_analysis(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    members = pmodels.DpMembers.objects.filter(del_flg='N')
    recentpayments = list(pmodels.Payment.objects.all())
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
    now = datetime.datetime.now()
    threeyearsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952*3)))
    twoyearsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952*2)))
    oneyearago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952)))
    sixmonthsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952/2)))
    monthlypayments = list(pmodels.DpPayments.objects.all())
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
    inactivemembers = []
    activemembers = []
    fairlyactivemembers = []
    domantmembers = []
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    for member in members:
        #  datetime(int(member.start_year),months.index(member.start_month)+1,1)

        join_date =  member.created_on
        if join_date:
            pass
        else:
            join_date = datetime.datetime(2005,1,1)
        payments = list(pmodels.Payment.objects.filter(partner = member))
        if len(payments) == 0:
            if join_date < sixmonthsago:
                domantmembers.append(member)
            else:
                activemembers.append(member)

        else:
            if join_date > sixmonthsago:
                activemembers.append(member)
            else:
                payments.reverse()
                monthlypayments = []
                for payment in payments:
                    for monthpay in payment.months.all():
                        monthlypayments.append(monthpay)            
                lastsixmonthspayments = list(filter(lambda x:x.month_covered >= sixmonthsago.date(), monthlypayments))
                if len(lastsixmonthspayments) >= 6:
                    activemembers.append(member)
                elif payments[0].date_time_added >= oneyearago:
                    fairlyactivemembers.append(member)
                elif payments[0].date_time_added <= twoyearsago:
                    inactivemembers.append(member)
                elif payments[0].date_time_added <= threeyearsago:
                    domantmembers.append(member)

    allObject['activemembers'] = len(activemembers)
    allObject['inactivemembers'] = len(inactivemembers)
    allObject['fairlyactivemembers'] = len(fairlyactivemembers)
    allObject['domantmembers'] = len(domantmembers)
    allObject['members'] = members
    allObject['monthpercentageincrease'] = monthpercentageincrease
    allObject['thismonthpaymentsamount'] ='{:,.2f}'.format(thismonthpaymentsamount)
    allObject['yearpercentageincrease'] = yearpercentageincrease
    allObject['thisyearpaymentsamount'] ='{:,.2f}'.format(thisyearpaymentsamount)
    template_name = 'padmin/members_analysis.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)



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
                    batchpayment.approved=True
                    batchpayment.save()
            partner.payment_synced = True
            partner.save()

    output_data = { 
                    'content':'Done',
                    # 'next_page':monthlypayments.next_page_number()
                    
                }
    return JsonResponse(output_data)



@login_required
def dashboard(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/dashboard.html'
    admin = allObject['admin']

    payments = list(pmodels.Payment.objects.filter(approved=True))
    payments.sort(key=lambda x:x.end_date,reverse=True)
    # monthlypayments = []
    # for payment in payments:
    #     for monthpayment in payment.months.all():
    #         monthlypayments.append(monthpayment)    
    # monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)
    # allObject['monthlypayments'] = monthlypayments[0:5]
    allObject['payments'] = payments[0:20]
    # pendingpayments = pmodels.Payment.objects.all()
    # allObject['pendingpayments'] = pendingpayments
    allObject['title'] = 'DPG | Dashboard'
    allObject['page'] = 'Dashboard'
    # allObject['twoyearsback'] = twoyearsback
    return render(request,template_name,allObject)


def filtermembers(request,partners,allObject):
    gender = str(request.POST.copy().get('gender'))
    all_age = str(request.POST.copy().get('all_age'))
    all_country =str(request.POST.copy().get('all_country'))
    all_status=str(request.POST.copy().get('all_status'))

    country =str(request.POST.copy().get('country'))
    all_account_type =str(request.POST.copy().get('all_account_type'))
    account_type =str(request.POST.copy().get('account_type'))
    status =str(request.POST.copy().get('status'))
    recentpayments = list(pmodels.Payment.objects.all())
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
    now = datetime.datetime.now()
    threeyearsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952*3)))
    twoyearsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952*2)))
    oneyearago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952)))
    sixmonthsago = datetime.datetime.fromtimestamp((datetime.datetime.timestamp(now) -(31556952/2)))
    inactivemembers = []
    activemembers = []
    fairlyactivemembers = []
    domantmembers = []
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    for member in partners:
        join_date =  member.created_on
        if join_date:
            pass
        else:
            join_date = datetime.datetime(2005,1,1)
        payments = list(pmodels.Payment.objects.filter(partner = member))
        if len(payments) == 0:
            if join_date < sixmonthsago:
                domantmembers.append(member)
            else:
                activemembers.append(member)

        else:
            if join_date >= sixmonthsago:
                activemembers.append(member)
            else:
                payments.reverse()
                monthlypayments = []
                for payment in payments:
                    for monthpay in payment.months.all():
                        monthlypayments.append(monthpay)            
                lastsixmonthspayments = list(filter(lambda x:x.month_covered >= sixmonthsago.date(), monthlypayments))
                if len(lastsixmonthspayments) >= 6:
                    activemembers.append(member)
                elif payments[0].date_time_added >= oneyearago:
                    fairlyactivemembers.append(member)
                elif payments[0].date_time_added <= twoyearsago:
                    inactivemembers.append(member)
                elif payments[0].date_time_added <= threeyearsago:
                    domantmembers.append(member)
    if all_status == 'all':
        bystatus = partners
    elif status == 'active':
        bystatus = activemembers
    elif status == 'inactive':
        bystatus = inactivemembers
    elif status == 'fairlyactive':
        bystatus = fairlyactivemembers
    elif status == 'domant':
        bystatus = domantmembers
    if all_age == 'all':
        byage = partners
    else:
        try:
            start_age_range = int(request.POST.copy().get('start_age_range'))
        except ValueError:
            start_age_range=1
        try:
            end_age_range = int(request.POST.copy().get('end_age_range'))
        except ValueError:
            end_age_range = 200
        now = datetime.datetime.now()
        byage =filter(lambda x:now.today().year - x.date_of_birth.year >= start_age_range and now.today().year - x.date_of_birth.year <= end_age_range,partners)
    all_join_period =  str(request.POST.copy().get('all_join_period'))
    join_start_date = str(request.POST.copy().get('from'))
    all_marital_status =  str(request.POST.copy().get('all_marital_status'))
    join_end_date = str(request.POST.copy().get('to'))
    marital_status = str(request.POST.copy().get('marital_status'))
    if all_join_period == 'all':
        bydatejoined = partners
    else:
        try:
            join_start_date_obj = datetime.datetime.strptime(join_start_date,'%Y-%m-%d').date()
        except ValueError:
            join_start_date_obj = datetime.datetime.strptime('2000-01-01','%Y-%m-%d').date()
        try:
            join_end_date_obj = datetime.datetime.strptime(join_end_date,'%Y-%m-%d').date()
        except ValueError:
            join_end_date_obj = datetime.datetime.now().date()
        bydatejoined =filter(lambda x:x.signup_date >=join_start_date_obj and x.signup_date <= join_end_date_obj,partners)
    if gender == 'all':
        bygender = partners
    elif gender != 'None':
        bygender =filter(lambda x:x.gender == gender,partners)
    else:
        bygender = []
    if all_marital_status == 'all':
        bymaritalstatus = partners
    elif marital_status != 'None':
        bymaritalstatus =filter(lambda x:x.marital_status == marital_status,partners)
    else:
        bymaritalstatus = []
    if all_country == 'all':
        bycountry = partners
    elif country != 'None':
        bycountry =filter(lambda x:x.country == country,partners)
    else:
        bycountry = []
    if all_account_type == 'all':
        byaccounttype = partners
    elif account_type != 'None':
        byaccounttype =filter(lambda x:x.account_type == account_type,partners)
    else:
        byaccounttype = []
    # filtered_members = byaccounttype

    filtered_members = list(set.intersection(set(byage),set(bystatus), set(bygender),set(bydatejoined),set(bymaritalstatus),set(byaccounttype),set(bycountry)))
    return filtered_members

@login_required
def filteredmembers(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/members.html'
    admin = allObject['admin']
    partners = list(pmodels.DpMembers.objects.filter(del_flg='N'))
    filtered_members =filtermembers(request, partners,allObject)
    allObject['members'] = filtered_members
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)


@login_required
def allpartners(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/all_partners.html'
    partners = pmodels.DpMembers.objects.all()
    allObject['partners'] =partners
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)
    

@login_required
def membersearch(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/members.html'
    query = request.POST.copy().get('query')
    admin = allObject['admin']
    partners = pmodels.DpMembers.objects.filter(member_no=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(phone_no=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(email_addres=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(first_name__contains=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(last_name__contains=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(first_name=query)
    if len(partners) <1:
        partners = pmodels.DpMembers.objects.filter(last_name=query)
    allObject['members'] =partners
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)



@login_required
def messagefilteredmembers(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/members.html'
    admin = allObject['admin']
    partners = list(pmodels.DpMembers.objects.filter(del_flg='N'))
    message =str(request.POST.copy().get('message'))
    subject =str(request.POST.copy().get('subject'))
    from django.utils.html import strip_tags
    filtered_members = filtermembers(request,partners,allObject)
    allObject['message']=message
    html_message = render_to_string('padmin/message_members.html',allObject)
    message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER 
    email_from = 'info@dominionpartners.com'
    recipient_list = ['info.chinecherem@gmail.com','kamsipearl@gmail.com','ogohifeoma@yahoo.com']
    # for member in filtered_members:
    #     recipient_list.append(member.email_addres)
    try:
        send_mail(subject,message, email_from, recipient_list, html_message=html_message,)
    except socket.gaierror:
        pass
    template_name = 'general/success.html'
    message = html_message
    allObject['message'] = 'Message sent successfully'
    successcontent = loader.render_to_string(template_name,allObject,request)
    allObject['message'] = message
    output_data = {
        'heading':'Action Required',
        'modal_message':successcontent
                    }        
                    
    return JsonResponse(output_data)


@login_required
def filteredmembersdownload(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    partners = list(pmodels.DpMembers.objects.filter(del_flg='N'))
    file_type =str(request.POST.copy().get('format'))
    filtered_members = filtermembers(request,partners,allObject)
    filename = 'DPG Members'
    if file_type == 'excel':
        data = [
            ['LAST NAME', 'FIRST NAME','PHONE NUMBER','EMAIL ADDRESS','RESIDENTIAL ADDRESS','DATE JOINED','ACCOUNT TYPE','LAST PAYMENT DATE']
        ]
        partner_details =[]
        for partner in filtered_members:
            partner_details.append(partner.last_name)
            partner_details.append(partner.first_name)
            partner_details.append(partner.phone_no)
            partner_details.append(partner.email_addres)
            partner_details.append(partner.full_address)
            partner_details.append(partner.signup_date)
            partner_details.append(partner.account_type)
            partner_details.append(partner.last_payment_date)

            data.append(partner_details)
            partner_details=[]
        return ExcelResponse(data, filename)
    elif file_type == 'pdf':
        allObject['members'] = filtered_members
        encoded_string = ''
        with open(allObject['settings'].logo.path, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read()).decode()
        logo= 'data:image/%s;base64,%s' % ('png', encoded_string)
        template_name = 'padmin/members_download.html'
        response = PDFTemplateResponse(request=request,
                                        template=template_name,
                                        filename=filename+".pdf",
                                        context= {'allObject':allObject,'logo':logo},
                                        show_content_in_browser=False,
                                        cmd_options={
                                            'page-size': 'A4',
                                            'margin-top': '0in',
                                            'margin-right': '0in',
                                            'margin-bottom': '0in',
                                            'margin-left': '0in',
                                            'encoding': "UTF-8",
                                            'no-outline': None,
                                        "zoom":1,
                                        
                                        'javascript-delay':1000,
                                        'footer-center' :'[page]/[topage]',
                                        "no-stop-slow-scripts":True},
                                        )
        return response



@login_required
def sortpaymentsfromdate(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/payment_search_results.html'
    admin = allObject['admin']
    recentpayments = list(pmodels.Payment.objects.all())
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
    payment_start_date = str(request.POST.copy().get('from'))
    payment_end_date = str(request.POST.copy().get('to'))
    payment_start_date_obj = datetime.datetime.strptime(payment_start_date,'%Y-%m-%d')
    payment_end_date_obj = datetime.datetime.strptime(payment_end_date,'%Y-%m-%d')
    monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__month__gte =payment_start_date_obj.month,month_covered__year__gte =payment_start_date_obj.year,month_covered__month__lte =payment_end_date_obj.month,month_covered__year__lte =payment_end_date_obj.year,))
    allObject['payments'] = monthlypayments
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
                    }
    return JsonResponse(output_data)





@login_required
def searchpayment(request,param=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/payment_search_results.html'
    query = request.POST.copy().get('query')
    admin = allObject['admin']
    recentpayments = list(pmodels.Payment.objects.filter(partner__first_name=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__last_name=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__first_name__contains=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__last_name__contains=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__phone_no__contains=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__phone_no=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__phone_no_alt__contains=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__phone_no_alt=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__email_addres__contains=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__email_addres=query))
    if len(recentpayments)<1:
        recentpayments = list(pmodels.Payment.objects.filter(partner__member_no=query))
    recentpayments.sort(key=lambda x:x.end_date,reverse=True)

    allObject['payments'] = recentpayments
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
            'header':'My Profile',
                    }
    return JsonResponse(output_data)



@login_required
def sortpayments(request,param=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/payment_search_results.html'
    admin = allObject['admin']
    recentpayments = list(pmodels.Payment.objects.all())
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
    if param == 'month':
        monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__month =datetime.datetime.today().month,
        month_covered__year =datetime.datetime.today().year,))
        allObject['payments'] = monthlypayments
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'My Profile',
                        }
        return JsonResponse(output_data)
    elif param == 'year':
        monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__year =datetime.datetime.today().year,))
        allObject['payments'] = monthlypayments
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'My Profile',
                        }
        return JsonResponse(output_data) 




@login_required
def sortedpaymenttofile(request,param = None, *args, **kwargs,):
    allObject = inherit(request, *args, **kwargs)

    admin = allObject['admin']
    recentpayments = list(pmodels.Payment.objects.all())
    recentpayments.sort(key=lambda x:x.date_time_added,reverse=True)
    # param = str(request.POST.copy().get('param'))
    file_type = str(request.POST.copy().get('format'))
    quick_period = str(request.POST.copy().get('period'))
    monthswords = ['','January','February','March','April','May','June','July','August','September','October','November','December']

    try:
        template_name = 'padmin/year_payment_download.html'
        payment_start_date = str(request.POST.copy().get('from'))
        payment_end_date = str(request.POST.copy().get('to'))
        payment_start_date_obj = datetime.datetime.strptime(payment_start_date,'%Y-%m-%d')
        payment_end_date_obj = datetime.datetime.strptime(payment_end_date,'%Y-%m-%d')
        monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__month__gte =payment_start_date_obj.month,month_covered__year__gte =payment_start_date_obj.year,month_covered__month__lte =payment_end_date_obj.month,month_covered__year__lte =payment_end_date_obj.year,))
        filename =str(monthswords[payment_start_date_obj.date().month])+' ' + str(payment_start_date_obj.date().year) + ' TO '+str(monthswords[payment_end_date_obj.date().month])+' ' + str(payment_end_date_obj.date().year)+' Payments'
        period = 'THE PERIOD OF ' + str(monthswords[payment_start_date_obj.date().month])+' ' + str(payment_start_date_obj.date().year) + ' TO '+str(monthswords[payment_end_date_obj.date().month])+' ' + str(payment_end_date_obj.date().year)
        allObject['payments'] = monthlypayments
        if file_type == 'excel':
            data = [
                ['PARTNER', 'AMOUNT','MONTH']
            ]
            payment_details =[]
            for payment in monthlypayments:
                # payment.save()
                # payment.refresh_from_db()
                try:
                    partner = pmodels.DpMembers.objects.get(member_no=payment.member_no)
                except ObjectDoesNotExist:
                    try:
                        partner = pmodels.DpMembers.objects.get(pk=payment.member_id)
                    except ObjectDoesNotExist:
                        partner = ''
                if partner:
                    payment_details.append(partner.first_name or 'none' +' ' +partner.last_name or 'none')
                else:
                    payment_details.append('Unknown')
                payment_details.append(payment.formatted_amount or payment.amount)
                payment_details.append(str(monthswords[payment.month_covered.month]))
                data.append(payment_details)
                payment_details=[]
            return ExcelResponse(data, filename)
    except ValueError:
        if quick_period == 'month':
            template_name = 'padmin/month_payment_download.html'

            period = 'THE MONTH OF ' + str(monthswords[datetime.datetime.today().month]) + ', '+str(datetime.datetime.today().year) 
            filename = str(monthswords[datetime.datetime.today().month]) + ', '+str(datetime.datetime.today().year)  +' Payments'
            monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__month =datetime.datetime.today().month,month_covered__year =datetime.datetime.today().year,))
            monthlypayments.sort(key=lambda x:x.month_covered,reverse=True)
            allObject['payments'] = monthlypayments
            if file_type == 'excel':
                data = [
                    ['PARTNER', 'AMOUNT',]
                ]
                payment_details =[]
                for payment in monthlypayments:
                    # payment.save()
                    # payment.refresh_from_db()
                    try:
                        partner = pmodels.DpMembers.objects.get(member_no=payment.member_no)
                    except ObjectDoesNotExist:
                        try:
                            partner = pmodels.DpMembers.objects.get(pk=payment.member_id)
                        except ObjectDoesNotExist:
                            partner = ''
                    if partner:
                        payment_details.append(partner.first_name +' ' +partner.last_name)
                    else:
                        payment_details.append('Unknown')
                    payment_details.append(payment.formatted_amount or payment.amount)
                    data.append(payment_details)
                    payment_details=[]
                return ExcelResponse(data, filename)
        elif quick_period == 'year':
            template_name = 'padmin/year_payment_download.html'
            filename = str(datetime.datetime.today().year)  +' Payments'
            period = 'THE YEAR ' +  str(datetime.datetime.today().year)
            monthlypayments = list(pmodels.DpPayments.objects.filter(month_covered__year =datetime.datetime.today().year,))
            monthlypayments.sort(key=lambda x:x.month_covered,reverse=True)
            allObject['payments'] = monthlypayments
            if file_type == 'excel':
                data = [
                    ['PARTNER', 'AMOUNT','MONTH']
                ]
                payment_details =[]
                for payment in monthlypayments:
                    # payment.save()
                    # payment.refresh_from_db()
                    try:
                        partner = pmodels.DpMembers.objects.get(member_no=payment.member_no)
                    except ObjectDoesNotExist:
                        try:
                            partner = pmodels.DpMembers.objects.get(pk=payment.member_id)
                        except ObjectDoesNotExist:
                            partner = ''
                    if partner:
                        payment_details.append(partner.first_name +' ' +partner.last_name)
                    else:
                        payment_details.append('Unknown')
                    payment_details.append(payment.formatted_amount or payment.amount)

                    payment_details.append(str(monthswords[payment.month_covered.month]))
                    data.append(payment_details)
                    payment_details=[]
                return ExcelResponse(data, filename)
    monthlypaymentstotal = 0
    for payment in monthlypayments:
        monthlypaymentstotal+=payment.amount
    allObject['monthlypaymentstotal'] = '{:,.2f}'.format(monthlypaymentstotal)
    allObject['period'] = period
        # content = loader.render_to_string(template_name,allObject,request)
    # import pdfkit
    # from django.http import HttpResponse

    # pdf = pdfkit.from_string(content, filename+".pdf")

    # return HttpResponse("Everything working good, check out the root of your project to see the generated PDF.")

    # return payments_to_pdf(template_name,allObject)
    encoded_string = ''
    with open(allObject['settings'].logo.path, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read()).decode()
    logo= 'data:image/%s;base64,%s' % ('png', encoded_string)
    response = PDFTemplateResponse(request=request,
                                       template=template_name,
                                       filename=filename+".pdf",
                                       context= {'allObject':allObject,'monthlypayments':monthlypayments,'logo':logo},
                                       show_content_in_browser=False,
                                       cmd_options={
                                           'page-size': 'A4',
                                        'margin-top': '0in',
                                        'margin-right': '0in',
                                        'margin-bottom': '0in',
                                        'margin-left': '0in',
                                        'encoding': "UTF-8",
                                        'no-outline': None,
                                       "zoom":1,
                                      
                                       'javascript-delay':1000,
                                       'footer-center' :'[page]/[topage]',
                                       "no-stop-slow-scripts":True},
                                       )
    return response

@login_required
def myprofile(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    template_name = 'padmin/profile.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
            'content':content,
            'header':'My Profile',
                    }
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  


@login_required
def memberprofile(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    template_name = 'padmin/profile.html'
    allObject['partner'] = partner
    content = loader.render_to_string(template_name,allObject,request)
    allObject['title'] = 'DPG | Partner Profile'
    allObject['page'] = 'Partner profile'
    output_data = {
            'content':content,
            'header':'Member Details',
                    }
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  


# def recentremittances(request,*args, **kwargs):
#     allObject = inherit(request, *args, **kwargs)
#     payments=list(pmodels.Payment.objects.all())
#     payments.sort(key =lambda x:x.date_time_added,reverse=True)
#     allObject = inherit(request, *args, **kwargs)
#     readypayments = list(filter(lambda x:x.updated==True and x.approved==True,payments))
#     pendingupdate =  list(filter(lambda x:x.updated==False,payments))
#     pendingapproval =  list(filter(lambda x: x.approved==False,payments))
#     page = request.GET.get('page', 2)

#     paginator = Paginator(readypayments, 5)
#     try:
#         payments = paginator.page(page)
#     except PageNotAnInteger:
#         payments = paginator.page(1)
#     except EmptyPage:
#         payments = paginator.page(paginator.num_pages)

#     allObject['pendingupdates'] = pendingupdate
#     allObject['pendingapprovals'] = pendingapproval
#     allObject['payments'] = payments
#     template_name = 'padmin/recent_remittances.html'
#     content = loader.render_to_string(template_name,allObject,request)
#     output_data = { 
#                     'content':content,
#                     # 'next_page':monthlypayments.next_page_number()
                    
#                 }
#     return JsonResponse(output_data)


@login_required
def recentremittances(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    payments=list(pmodels.Payment.objects.all())
    payments.sort(key =lambda x:x.end_date,reverse=True)
    readypayments = list(filter(lambda x:x.updated==True and x.approved==True,payments))
    readypayments.sort(key =lambda x:x.end_date,reverse=True)

    pendingupdate =  list(filter(lambda x:x.updated==False,payments))
    pendingapproval =  list(filter(lambda x: x.approved==False,payments))
    page = request.GET.get('page', 2)

    paginator = Paginator(readypayments, 5)
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



def partnersallpayments(request,userid=None, *args, **kwargs):
    from partners.views import allpayments as partnersallpayments
    return partnersallpayments(request, userid,*args, **kwargs)



@login_required
def memberpage(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    visits =  list(pmodels.VisitorsLog.objects.filter(memberid=userid))
    # from partners.views import allpayments
    # allpayments(partner,allObject)
    template_name = 'padmin/member_page.html'
    allObject['partner'] = partner
    allObject['visits'] = len(visits)
    content = loader.render_to_string(template_name,allObject,request)
    allObject['title'] = "DPG | Partner's Page"
    allObject['page'] = 'Partner Overview'
    output_data = {
            'content':content,
            'header':'Member Details',
                    }
    return render(request,template_name,allObject)
    return JsonResponse(output_data)  



@login_required
def recordpayment(request,userid=None, *args, **kwargs):
    allObject = inherit(request)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    allObject['partner'] = partner
    paymentid = request.GET.get('tx_ref')
    referenceid = request.GET.get('transaction_id')
    status = request.GET.get('status')
    payment = pmodels.Payment.objects.get(paymentid=paymentid,partner=partner)
    payment.referenceid = referenceid
    payment.status = status
    if status =='successful':
        payment.approved = True

    payment.save()
    return redirect('admin_member_page',userid=partner.member_no)


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
                coveredmonth.month_covered=year+'-'+month+'-'+day
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
                coveredmonth.month_covered=year+'-'+month+'-'+day
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
                coveredmonth.month_covered=year+'-'+month+'-'+day
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
            coveredmonth.month_covered=year+'-'+month+'-'+day
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
                        coveredmonth.month_covered=year+'-'+month+'-'+day
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
def makepayment(request,userid=None, *args, **kwargs):
    allObject = inherit(request)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    allObject['partner'] = partner
    if request.method == 'POST':
        payment = pforms.makepayment(request.POST)
        if payment.is_valid:
            payment.save(commit=False)
            payment=payment.instance
            payment.partner = partner
            payment.save()
            updatecurrentpayment(request,payment,partner)        
            output_data = { 
                            'pay':True,
                            'amount':payment.amount,  
                            'paymentid':payment.paymentid,                          
                            'currency':payment.currency,                           
                        }
            return JsonResponse(output_data)
    else:
           
        template_name = 'padmin/make_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Pay now',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)



import socket
 
@login_required
def updatememberprofile(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    allObject['partner'] = partner
    allObject['page'] = 'Profile update'

    if request.method == 'POST':
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
            partner.save()
            message = "Your profile has been successfully updated. If you didn't perform this action, kindly contact Dominion Partners to report this action. Thank yoo"
            partner.profile_updated = True
            partner.save()
            if str(request.POST.copy().get('email')) != partner.email_addres:
                partner.previous_email = partner.email_addres
                partner.email_addres=str(request.POST.copy().get('email'))
                partner.email_confirmed= False
                partner.save()
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
                recipient_list = [partner.email_addres, ]
                try:
                    send_mail( subject, message, email_from, recipient_list )
                except socket.gaierror:
                    pass
                template_name = 'partners/email_confirmation_form.html'
                content = loader.render_to_string(template_name,allObject,request)
                message = 'Your profile was updated successfully'
                allObject['message'] = message
                successcontent = loader.render_to_string(template_name,allObject,request)
                allObject['message'] = message
                output_data = {
                    'heading':'Action Required',
                    'modal_content':content,
                    'next_url':request.POST.copy().get('next'),

                    'message':message
                                }        
                                
                return JsonResponse(output_data)
            profile_updated = True
            subject = 'Profile Updated'
            mail_body = 'Your profile has been updated'
            message = render_to_string('partners/update_profile_email.html', {
                'message':mail_body,
                'user':partner.user
                })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [partner.email_addres, ] 
            # send_mail( subject, message, email_from, recipient_list ) 
            template_name = 'general/success.html'
            content = loader.render_to_string(template_name,allObject,request)
            message = 'Your profile was updated successfully'
            allObject['message'] = message
            successcontent = loader.render_to_string(template_name,allObject,request)
            allObject['message'] = message
            output_data = {
                'done':True,
                'content':content,
                'next_url':request.POST.copy().get('next'),

                'modal_message':successcontent,
                            }        
                            
            return JsonResponse(output_data)

    else:
        allObject['next'] = request.GET.get('next') or redirect('admin_member_profile',userid=userid).url

        template_name = 'padmin/update_profile.html'
        tvstations = list(pmodels.TvStation.objects.all())
        allObject['tvstations'] = tvstations
        allObject['title'] = 'Update Profile - DPG'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                            'modal_content':content,
                            'heading':'Update Profile'
                        }
        return render(request,template_name,allObject)

        return JsonResponse(output_data)    



@login_required
def adminselectaccounttype(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)
    allObject['partner'] = partner
    allObject['title'] = 'DPG | Account selection'
    allObject['page'] = 'Account selection'

    if request.method == 'POST':
        if not partner.account_type == str(request.POST.copy().get('accounttype')):
            partner.photo = ''
            partner.profile_updated=False 
        partner.account_type=str(request.POST.copy().get('accounttype'))
        partner.account_type_selected=True

        partner.save()
        return redirect('admin_update_member_profile',userid=partner.member_no)
    template_name = 'padmin/select_account_type.html'
    return render(request,template_name,allObject)


# @login_required
# def adminselectaccounttype(request,userid=None, *args, **kwargs):
#     allObject = inherit(request, *args, **kwargs)
#     partner =  pmodels.DpMembers.objects.get(member_no=userid)
#     allObject['partner'] = partner
#     allObject['title'] = 'Select Account Type - DPG'

#     if request.method == 'POST':
#         if not partner.account_type == str(request.POST.copy().get('accounttype')):
#             partner.photo = ''        
#         partner.account_type=str(request.POST.copy().get('accounttype'))
#         partner.account_type_selected=True

#         partner.save()
#     template_name = 'padmin/profile_template.html'
#     content = loader.render_to_string(template_name,allObject,request)
#     output_data = {
#                         'content':content,
#                     }
#     # return render(request,template_name,allObject)
#     return JsonResponse(output_data)  

# def updatememberprofile(request,userid=None, *args, **kwargs):
#     allObject = inherit(request, *args, **kwargs)
#     partner =  pmodels.DpMembers.objects.get(member_no=userid)
#     allObject['partner'] = partner
#     if request.method == 'POST':
#         admin =allObject['admin']
#         # secretanswer = str(request.POST.copy().get('sqa'))
#         # secretquestion =str(request.POST.copy().get('sq'))
#         phone = str(request.POST.copy().get('phone'))
#         number = str(request.POST.copy().get('street_number'))
#         street = str(request.POST.copy().get('street'))
#         city = str(request.POST.copy().get('city'))
#         lga = str(request.POST.copy().get('lga'))
#         state= str(request.POST.copy().get('state'))
#         nearest_bus_stop= str(request.POST.copy().get('busstop'))
#         landmark= str(request.POST.copy().get('landmark'))
#         dob = request.POST.copy().get('dob')
#         currency = str(request.POST.copy().get('currency'))
#         monthly_support= int(request.POST.copy().get('monthly_support'))
#         gender= str(request.POST.copy().get('gender'))
#         marriage= str(request.POST.copy().get('marriage'))
#         cgcc= str(request.POST.copy().get('cgcc'))
#         # partner.secret_question = secretquestion
#         # partner.secret_answer = secretanswer
#         partner.phone_no = phone
#         partner.lga = lga
#         partner.state = state
#         partner.street_number = number
#         partner.city = city
#         partner.street = street
#         partner.nearest_bus_stop = nearest_bus_stop
#         partner.landmark = landmark
#         partner.date_of_birth = dob
#         partner.currency = currency
#         partner.monthly_support =monthly_support
#         partner.gender = gender
#         partner.marital_status = marriage
#         if cgcc == 'yes':
#             partner.is_cgcc_member = True
#         partner.save()
#         partner.refresh_from_db()
#         partner.first_name = str(request.POST.copy().get('first_name'))
#         partner.last_name = str(request.POST.copy().get('last_name'))
#         partner.email=str(request.POST.copy().get('email'))
#         partner.save()
#         message = "Your profile has been successfully updated"
#         partner.profile_updated = True
#         partner.save()
#         profile_updated = True
#         subject = 'Profile Updated'
#         mail_body = 'Your profile has been updated'
#         template_name = 'general/success.html'
#         allObject['message'] = 'Your profile was updated successfully'
#         successcontent = loader.render_to_string(template_name,allObject,request)
#         template_name = 'padmin/dashboard_content.html'
#         content = loader.render_to_string(template_name,allObject,request)
#         output_data = {
#             'done':True,
#              'content':content,
#              'modal_message':successcontent,
#              'heading':'Due balance: ' + 'N2000'
#                         }
#         message = render_to_string('padmin/update_profile_email.html', {
#                'message':mail_body,
#                'user':user
#             })
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [user.email, ] 
#         # send_mail( subject, message, email_from, recipient_list ) 
#         return JsonResponse(output_data)    

#     else:
#         admin =allObject['admin']   
#         template_name = 'padmin/update_profile.html'
#         content = loader.render_to_string(template_name,allObject,request)
#         output_data = {
#                             'modal_content':content,
#                             'heading':'Update Profile'
#                         }
#         return render(request,template_name,allObject)
#         return JsonResponse(output_data)    



@login_required
def dashboardcontent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        template_name = 'padmin/dashboard_content.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'Due balance: ' + 'N2000',
                        }
        return JsonResponse(output_data)  
    else:
        return updateprofileform(request, *args, **kwargs)


@login_required
def informationdeskcontent(request,content=None,cid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        try:
            if str(content).lower() == 'article':
                reqcontent = pmodels.Article.objects.get(contentid=cid)
            elif str(content).lower() == 'announcement':
                reqcontent = pmodels.Announcement.objects.get(contentid=cid)
            template_name = 'padmin/information_desk_content.html'
            allObject['content']=reqcontent
            content = loader.render_to_string(template_name,allObject,request)
            output_data = {
                    'modal_content':content,
                    'heading':reqcontent.title,
                            }
            return JsonResponse(output_data) 
        except ObjectDoesNotExist:
            output_data = {
            'content':'Content not found',
                    }
            return JsonResponse(output_data)   
         
    else:
        return updateprofileform(request, *args, **kwargs)


@login_required
def events(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
        try:
            todaysevent = pmodels.Event.objects.get(end_date_time__gt=datetime.now(),start_date_time__date=datetime.datetime.today().date())
            if todaysevent.start_date_time < datetime.datetime.now() and todaysevent.end_date_time > datetime.datetime.now():
                allObject['eventongoing'] =True         
        except ObjectDoesNotExist:
            todaysevent=''
            allObject['eventongoing'] =False
        upcomingevents.sort(key=lambda x: x.date_time_added,reverse=True)

        allObject['upcomingevents'] =upcomingevents
        pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.now()))
        pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['pastevents'] =pastevents
        allObject['todaysevent'] =todaysevent
        template_name = 'padmin/events.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'content':content,
                'header':'Events',
                        }
        return render(request,template_name,allObject)
        return JsonResponse(output_data)  
    else:
        return updateprofileform(request, *args, **kwargs)




@login_required
def announcements(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        announcements =  list(pmodels.Announcement.objects.all())
        announcements.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['announcements'] =announcements
        template_name = 'padmin/announcements.html'
        # content = loader.render_to_string(template_name,allObject,request)
        # output_data = {
        #         'content':content,
        #         'header':'Announcements',
        #                 }
        # return JsonResponse(output_data)  
        return render(request,template_name,allObject)

    else:
        return updateprofileform(request, *args, **kwargs)




@login_required
def announcementdetails(request,announcementid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        announcement = pmodels.Announcement.objects.get(contentid=announcementid)
        allObject['announcement'] = announcement
        template_name = 'padmin/announcement_details.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
                'heading':announcement.title,
                'modal_content':content,
                        }
        return JsonResponse(output_data)  
    else:
        return updateprofileform(request, *args, **kwargs)





@login_required
def eventregistration(request,eventid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        event = pmodels.Event.objects.get(eventid=eventid)
        event.registrations.add(partner)
        event.save()
        upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
        upcomingevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['upcomingevents'] =upcomingevents
        pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.now()))
        pastevents.sort(key=lambda x: x.date_time_added,reverse=True)
        allObject['pastevents'] =pastevents
        template_name = 'padmin/events.html'
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
        return updateprofileform(request, *args, **kwargs)

from qr_code.qrcode.utils import QRCodeOptions
@login_required
def eventdetails(request,eventid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        event = pmodels.Event.objects.get(eventid=eventid)
        allObject['event'] = event
        input_data = str(event.eventid)
        template_name = 'padmin/payment_details.html'
        context = dict(
               qrc_options= QRCodeOptions(event.eventid,size='18', border=8, error_correction='L',image_format='png', ),
            )
        content = loader.render_to_string(template_name,context,request)
        output_data = {
                'message':content,
                        }
        return JsonResponse(output_data)  
    else:
        return updateprofileform(request, *args, **kwargs)




@login_required
def verifyevent(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    if partner.profile_updated:
        try:
            event = pmodels.Event.objects.get(eventid=request.GET.get('eventid'))
            ongoingevents = list(pmodels.Event.objects.filter(end_date_time__gt = datetime.datetime.now(),start_date_time__lt=datetime.now()))
            upcomingevents =  list(pmodels.Event.objects.filter(start_date_time__gt = datetime.datetime.now()))
            pastevents =  list(pmodels.Event.objects.filter(end_date_time__lt = datetime.datetime.now(),start_date_time__lt=datetime.now()))
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
        return updateprofileform(request, *args, **kwargs)





def videos(request, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    videos = list(pmodels.Video.objects.all())
    videos.sort(key=lambda x: x.date_time_added,reverse=True)
    allObject['latestvideo'] = videos[0]
    allObject['videos'] =videos
    template_name = 'padmin/videos.html'
    content = loader.render_to_string(template_name,allObject,request)
    output_data = {
        'content':content,
                        }
    return render(request,template_name,allObject)

    return JsonResponse(output_data)



    
@login_required
def sendmessage(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    template_name = 'padmin/send_message.html'  
    return render(request,template_name,allObject)




    
@login_required
def payments(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    # payments=list(pmodels.Payment.objects.all())
    # payments.sort(key =lambda x:x.date_time_added,reverse=True)
    # payments=list(pmodels.Payment.objects.filter(updated=True))
    # monthlypayments = []
    allObject['title']='DPG | Payments'
    allObject['page'] = 'Payments'
    # for payment in payments:
    #     for monthpayment in payment.months.all():
    #         monthlypayments.append(monthpayment)    
    # monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)
    # allObject['payments'] = monthlypayments[0:5]
    # pendingpayments = pmodels.Payment.objects.filter(updated=False)
    # allObject['pendingpayments'] = pendingpayments
    template_name = 'padmin/all_payments.html'  
    return render(request,template_name,allObject)



    
@login_required
def members(request,*args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    admin = allObject['admin']
    # partners = list(pmodels.DpMembers.objects.filter(del_flg='N'))
    # partners.sort(key=lambda x:x.last_name[0])
    # allObject['partners'] = partners[:10]
    template_name = 'padmin/all_members.html'  
    allObject['title'] = 'Members - DPG'
    allObject['page'] = 'Members'

    return render(request,template_name,allObject)


def adminmembercreation(request,*args, **kwargs):
    if request.method == 'POST':
        nums = '0123456789'
        tempnums = ''
        lalph = 'abcdefghijklmnopqrstuvwxyz'
        templalph=''
        ualph = lalph.upper()
        tempualph = ''
        # schars ='!@:;$%&*.,'
        tempschars =''

        for num in range(0,len(nums)):
            tempnums +=nums[round((random()-0.5)*len(nums))]
        for num in range(0,len(lalph)):
            templalph +=lalph[round((random()-0.5)*len(lalph))]
        for num in range(0,len(ualph)):
            tempualph +=ualph[round((random()-0.5)*len(ualph))]
        # for num in range(0,len(schars)):
        #     tempschars +=schars[round((random()-0.5)*len(schars))]
        temporary_password = tempnums[0:4] + templalph[0:3]+tempualph[0:3]+tempschars[0:3]
        password= []
        for char in temporary_password:
            password.insert(round(random()*5),char)
        password = ''.join(password)
        username = str(request.POST.copy().get('username')).lower()
        if username =='' or username ==' ' or username[0] ==' ':
            username = str(request.POST.copy().get('last_name')).lower()+str(request.POST.copy().get('first_name')).lower()
        email =str(request.POST.copy().get('email')).lower()
        formerrors = []
        try:
            user = User.objects.get(username=username)
            username = email
            # formerrors.append('<li>username already taken</li>')
        except ObjectDoesNotExist:
            pass
        try:
            user = User.objects.get(email=str(request.POST.copy().get('email')))
            formerrors.append('<li>Email already taken</li>')
        except ObjectDoesNotExist:
            pass
        # for error in form.errors:
        #     formerrors.append(error)
        #     formerrors.append(form.errors[error])
        erroroutput ="<ul class='text-danger p-0'>"
        errorlist = ''
        if len(formerrors) >0:
            for error in formerrors:
                errorlist += '<li>' +str(error)+'</li>'
            erroroutput += errorlist + '</ul>'
            output_data = { 
                            'invalid':True,
                            'message':'<b>Ooops... Something is wrong!</b>' + erroroutput,
                            
                        }
            return JsonResponse(output_data)
        harshed_password = make_password(password)
        user = User.objects.create(password=harshed_password, username=username, 
        first_name =str(request.POST.copy().get('first_name')),last_name= str(request.POST.copy().get('last_name')),
        email= email)
        user_id = 'SC'+str(round(random()*123456789090929))
        user_id = user_id[0:10]
        # form.user_id = user_id
        chars = '0123456789' 
        token = ''
        for num in range(0,len(chars)):
            token = token +chars[round((random()-0.5)*len(chars))]
        token = token[0:6]                
        pmodels.DpMembers.objects.create(first_name = user.first_name,last_name=user.last_name,email_addres=user.email, user=user.pk,userid=user_id,last_token=make_password(token),temporary_password=True)
        subject = 'welcome to Dominion Partners'
        current_site = Site.objects.get_current()
        message = render_to_string('allauth/account/email_confirm.html', {
                'token': token,
            })
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [user.email, ]
        try:
            send_mail( subject, message, email_from, recipient_list )
        except socket.gaierror:
            pass
        subject = 'Login Details - DPG'
        current_site = Site.objects.get_current()
        message = render_to_string('allauth/account/default_password.html', {
                'password': password,
                'username': username,
                'email':email,
            })
        recipient_list = [user.email, ]
        try:
            send_mail( subject, message, email_from, recipient_list )
        except socket.gaierror:
            pass
        user.is_active = True
        user.save()

        template_name = 'general/success.html'
        # content = loader.render_to_string(template_name,allObject,request)
        message = """Member successfully created <br> Member default Login details are <br> 
       """+'<div class="h2 text-dark">Password: '+password+'</div>' +'<div class="h2 text-dark">Username: '+username+'</div>'
        allObject['message'] = message
        successcontent = loader.render_to_string(template_name,allObject,request)
        output_data = {
            'done':True,
            # 'content':content,
            'modal_message':successcontent,
                        }        
                        
        return JsonResponse(output_data)
    else:
        # allObject['password']=password
        template_name = 'padmin/create_member.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = {
            'heading':'Member Creation',
            'modal_content':content,
                        }        
                        
        return JsonResponse(output_data)


@login_required
def updatepayment(request,paymentid=None, *args, **kwargs):
    allObject = inherit(request)
    admin = allObject['admin']
    payment = pmodels.Payment.objects.get(paymentid=paymentid,admin=admin)
    if request.method == 'POST':
        # parent_thumbnail = str(request.POST.copy().get('parent_thumbnail'))
        # day = uforms.addeventday(request.POST,request.FILES)
        end_date_time_str = str(request.POST.copy().get('end_date_time'))
        end_date_time_obj = datetime.datetime.strptime(end_date_time_str, '%m/%d/%Y %I:%M %p')
        start_date_time_str = str(request.POST.copy().get('start_date_time'))
        start_date_time_obj = datetime.datetime.strptime(start_date_time_str, '%m/%d/%Y %I:%M %p')
        amount = int(request.POST.copy().get('amount'))
        payment = pmodels.Payment.objects.filter(paymentid=paymentid,admin=admin).update(end_date_time=end_date_time_obj,
        start_date_time=start_date_time_obj,)
        payment=pmodels.Payment.objects.get(paymentid=paymentid)
        periodcounter = end_date_time_obj.month - start_date_time_obj.month
        counter = 0
        monthlyamount = amount/(periodcounter+1)
        for month in range(1,periodcounter+2):
            if counter == 0:
                coveredmonth = pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,month_covered=start_date_time_obj,paymentid=payment.paymentid)
                counter +=1
                payment.months.add(coveredmonth)
            elif month-1 + start_date_time_obj.month == end_date_time_obj.month:
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,paymentid=payment.paymentid)
                year = str(start_date_time_obj.year)
                month = str(start_date_time_obj.month +month-1)
                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.month_covered=year+'-'+month+'-'+day
                coveredmonth.save()
                payment.months.add(coveredmonth)
                break
            else:
                # dateobject = datetime.datetime.date()
                coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,paymentid=payment.paymentid)
                year = str(start_date_time_obj.year)
                month = str(start_date_time_obj.month + month-1)
                day = str(1)
                coveredmonth.refresh_from_db()
                coveredmonth.month_covered=year+'-'+month+'-'+day
                coveredmonth.save()
                payment.months.add(coveredmonth)
        payment.updated=True
        payment.save()
        payment.refresh_from_db()
        payment_details_template = 'padmin/payments.html'
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
        template_name = 'padmin/update_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Update Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)



# @login_required
# def createpayment(request,action=None, *args, **kwargs):
#     allObject = inherit(request)
#     admin = allObject['admin']

#     if request.method == 'POST':
#         # parent_thumbnail = str(request.POST.copy().get('parent_thumbnail'))
#         # day = uforms.addeventday(request.POST,request.FILES)
#         end_date_time_str = str(request.POST.copy().get('end_date_time'))
#         end_date_time_obj = datetime.datetime.strptime(end_date_time_str, '%m/%d/%Y %I:%M %p')
#         start_date_time_str = str(request.POST.copy().get('start_date_time'))
#         start_date_time_obj = datetime.datetime.strptime(start_date_time_str, '%m/%d/%Y %I:%M %p')
#         amount = int(request.POST.copy().get('amount'))
#         payment = pmodels.Payment.objects.create( amount=amount, end_date_time=end_date_time_obj,
#         start_date_time=start_date_time_obj,)
#         payment.refresh_from_db()
#         periodcounter = end_date_time_obj.month - start_date_time_obj.month
#         counter = 0
#         monthlyamount = amount/(periodcounter+1)
#         for month in range(1,periodcounter+2):
#             if counter == 0:
#                 coveredmonth = pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,month_covered=start_date_time_obj,paymentid=payment.paymentid)
#                 counter +=1
#                 payment.months.add(coveredmonth)
#             elif month-1 + start_date_time_obj.month == end_date_time_obj.month:
#                 coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,paymentid=payment.paymentid)
#                 year = str(start_date_time_obj.year)
#                 month = str(start_date_time_obj.month +month-1)
#                 day = str(1)
#                 coveredmonth.refresh_from_db()
#                 coveredmonth.month_covered=year+'-'+month+'-'+day
#                 coveredmonth.save()
#                 payment.months.add(coveredmonth)
#                 break
#             else:
#                 # dateobject = datetime.datetime.date()
#                 coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,amount=monthlyamount,paymentid=payment.paymentid)
#                 year = str(start_date_time_obj.year)
#                 month = str(start_date_time_obj.month + month-1)
#                 day = str(1)
#                 coveredmonth.refresh_from_db()
#                 coveredmonth.month_covered=year+'-'+month+'-'+day
#                 coveredmonth.save()
#                 payment.months.add(coveredmonth)
#         payment.updated=True
#         payment.save()
#         payment.refresh_from_db()
#         if action == 'next':
#             template_name = 'padmin/create_payment.html'
#             content = loader.render_to_string(template_name,allObject,request)
#             payment_details_template = 'padmin/payments.html'
#             payment_details = loader.render_to_string(payment_details_template,allObject,request)
#             output_data = { 
#                             'done':True,
#                             'message':'Payment added',
#                             'modal_content':content,
#                             'content':payment_details,
#                             'next':True
                            
#                         }
#             return JsonResponse(output_data)
#         elif action =='exit':
#             payment_details_template = 'padmin/payments.html'
#             payment_details = loader.render_to_string(payment_details_template,allObject,request)
#             output_data = { 
#                             'done':True,
#                             'message':'Payment added',
#                             'content':payment_details,
#                             'exit':True
                            
#                         }
#             return JsonResponse(output_data)
#     else:
           
#         template_name = 'padmin/create_payment.html'
#         content = loader.render_to_string(template_name,allObject,request)
#         output_data = { 
#                         'heading':'Create Payment',
#                         'modal_content':content,
                        
#                     }
#         return JsonResponse(output_data)


@login_required
def createpaymentlite(request,userid=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    partner =  pmodels.DpMembers.objects.get(member_no=userid)                  
    allObject['partner'] = partner
    # parent_thumbnail = str(request.POST.copy().get('parent_thumbnail'))
    if request.method == 'POST':
        payment = pforms.makepayment(request.POST)
        if payment.is_valid:
            payment.save(commit=False)
            payment=payment.instance
            payment.partner = partner
            payment.approved=True
            payment.save()
            updatecurrentpayment(request,payment,partner)                        
            payment.refresh_from_db()
            from partners.views import allpayments
            allpayments(request,userid)
            template_name = 'partners/payments.html'  
            payment_records = loader.render_to_string(template_name,allObject,request)
            template_name = 'general/success.html'
            allObject['message'] = 'Payment created successfully'
            successcontent = loader.render_to_string(template_name,allObject,request)
            output_data = { 
                            'modal_message':successcontent,
                            'content':payment_records,
                        }
            return JsonResponse(output_data)
    else:
           
        template_name = 'padmin/create_payment_lite.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Create Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)

@login_required
def createpayment(request,action=None, *args, **kwargs):
    allObject = inherit(request, *args, **kwargs)
    if request.method == 'POST':
        userid=str(request.POST.copy().get('userid')).lower()
        try:
            partner =  pmodels.DpMembers.objects.get(email_addres=userid)
        except ObjectDoesNotExist:
            try:
                partner =  pmodels.DpMembers.objects.get(phone_no=userid)
            except ObjectDoesNotExist:
                try:
                    partner =  pmodels.DpMembers.objects.get(member_no=userid)
                except ObjectDoesNotExist:
                    output_data = { 
                                'done':False,
                                'message':'user Not Found',                            
                            }
                    return JsonResponse(output_data)                    
        allObject['partner'] = partner
        # parent_thumbnail = str(request.POST.copy().get('parent_thumbnail'))
        payment = pforms.createpayment(request.POST)
        if payment.is_valid:
            payment.save(commit=False)
            # end_date_time_str = str(request.POST.copy().get('end_date_time'))
            # end_date_time_obj = datetime.datetime.strptime(end_date_time_str, '%m/%d/%Y %I:%M %p')
            # start_date_time_str = str(request.POST.copy().get('start_date_time'))
            # start_date_time_obj = datetime.datetime.strptime(start_date_time_str, '%m/%d/%Y %I:%M %p')
            # payment = pmodels.Payment.objects.create(partner=partner, amount=amount, end_date_time=end_date_time_obj,
            # start_date_time=start_date_time_obj,)
            # payment.refresh_from_db()
            payment=payment.instance
            payment.partner = partner
            payment.approved=True
            payment.save()
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
            while currentmonth < 13:
                if currentmonth ==12:
                    coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,paymentid=payment.paymentid,partner=partner)
                    year = str(currentyear)
                    month = str(currentmonth)

                    day = str(1)
                    coveredmonth.refresh_from_db()
                    coveredmonth.payment_month = months[int(month)-1]
                    coveredmonth.payment_year = year                 
                    coveredmonth.month_covered=year+'-'+month+'-'+day
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
                    coveredmonth =pmodels.DpPayments.objects.create(member_no=partner.member_no,paymentid=payment.paymentid,partner=partner)
                    year = str(currentyear)
                    month = str(currentmonth)

                    day = str(1)
                    coveredmonth.refresh_from_db()
                    coveredmonth.payment_month = months[int(month)-1]
                    coveredmonth.payment_year = year                
                    coveredmonth.month_covered=year+'-'+month+'-'+day
                    coveredmonth.save()
                    payment.months.add(coveredmonth)
                    message='never entered first loop'
                    if payment.end_date.year == currentyear and payment.end_date.month == currentmonth:
                        break
                    currentmonth +=1
            monthsamount =payment.amount/payment.months.count()
            for monthlypayment in payment.months.all():
                monthlypayment.amount = monthsamount
                monthlypayment.save()
                
            payment.updated=True
            payment.save()
            payment.refresh_from_db()

            if action == 'next':
                template_name = 'padmin/create_payment.html'
                content = loader.render_to_string(template_name,allObject,request)
                payments=list(pmodels.Payment.objects.all())
                payments.sort(key =lambda x:x.date_time_added,reverse=True)
                payments=list(pmodels.Payment.objects.filter(updated=True))
                monthlypayments = []
                for payment in payments:
                    for monthpayment in payment.months.all():
                        monthlypayments.append(monthpayment)    
                monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)
                allObject['payments'] = monthlypayments[0:5]
                pendingpayments = pmodels.Payment.objects.filter(updated=False)
                allObject['pendingpayments'] = pendingpayments
                template_name = 'padmin/all_payments.html'  
                all_payments = loader.render_to_string(template_name,allObject,request)
                output_data = { 
                                'done':True,
                                'message':'Payment added',
                                'modal_content':content,
                                'content':all_payments,
                                'next':True
                                
                            }
                return JsonResponse(output_data)
            elif action =='exit':
                payments=list(pmodels.Payment.objects.all())
                payments.sort(key =lambda x:x.date_time_added,reverse=True)
                payments=list(pmodels.Payment.objects.filter(updated=True))
                monthlypayments = []
                for payment in payments:
                    for monthpayment in payment.months.all():
                        monthlypayments.append(monthpayment)    
                monthlypayments.sort(key =lambda x:x.date_time_added,reverse=True)
                allObject['payments'] = monthlypayments[0:5]
                pendingpayments = pmodels.Payment.objects.filter(updated=False)
                allObject['pendingpayments'] = pendingpayments
                template_name = 'padmin/all_payments.html'  
                all_payments = loader.render_to_string(template_name,allObject,request)
                output_data = { 
                                'done':True,
                                'message':'Payment added',
                                'content':all_payments,
                                'exit':True  
                            }
                return JsonResponse(output_data)
    else:
           
        template_name = 'padmin/create_payment.html'
        content = loader.render_to_string(template_name,allObject,request)
        output_data = { 
                        'heading':'Create Payment',
                        'modal_content':content,
                        
                    }
        return JsonResponse(output_data)
