from typing import Text
from django.db.models.enums import Choices
from django.db.models.fields import TextField
from django_countries.fields import CountryField
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import (
    get_available_image_extensions,
    FileExtensionValidator,
)
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
import datetime
from django.shortcuts import get_object_or_404
from imagekit.models import ImageSpecField # < here
from pilkit.processors import ResizeToFill
from random import random
from tinymce.models import HTMLField
import os
import base64
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# from users import models as cmodels
from general import models as gmodels
from django.utils.timezone import now



class VisitorsLog(models.Model):
    ip_1 = models.TextField(default='',max_length = 200,blank=False)
    ip_2 = models.TextField(default='',max_length = 200,blank=False)
    ip_3 = models.TextField(default='',max_length = 200,blank=False)
    host_name = models.TextField(default='',max_length = 200,blank=False)
    url = models.URLField(blank=False)
    date_time_added = models.DateTimeField(auto_now=True,blank=True)
    memberid=models.CharField(default='',max_length=50,blank=True)
    location = models.TextField(max_length=1000,default='',blank=True)

    def __str__(self):
        return self.ip_1 or self.ip_2

    # def save(self,*args,*kwargs):



class DpMembers(models.Model):

    company_name = models.CharField(max_length=550,default='',blank=True)
    spouse_email = models.EmailField(default='',blank=True)
    marital_status = models.CharField(max_length =225, choices=(('S','Single'), ('M','Married'),('D','Divorced'), ('W','Widowed'),('P','Private')), default='',blank=False)
    gender = models.CharField(max_length =225, choices=(('M','Male'), ('F','Female')), default='',blank=False)
    date_of_birth = models.DateField(auto_now=False,default=now)
    spouse_dob = models.DateField(auto_now=False,default=now)
    spouse_phone= models.CharField(max_length=15, default='', blank=True,verbose_name='Phone Number 2')

    # landmark = models.CharField(max_length=225, default='',blank=False)
    # nearest_bus_stop = models.CharField(max_length=225, default='',blank=False)
    city = models.CharField(max_length=225, default='',blank=False)
    # lga = models.CharField(max_length=225, default='',blank=False)
    country = CountryField(default='',blank_label='(select country)')
    state = models.CharField(max_length=225, default='',blank=False)
    currency =  models.CharField(default='',choices=(('NGN','Naira'), ('USD','Dollar'),('GBP','Pounds'), ('EUR','Euro')), blank=True,max_length=500)
    member_no = models.CharField(max_length=45)
    title = models.CharField(max_length=5, blank=True, null=True, default='')
    middle_name = models.CharField(max_length=45, blank=True, null=True, default='')
    first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    email_addres = models.CharField(max_length=255, blank=True, default='')
    user_name = models.CharField(max_length=255, blank=True, null=True, default='')
    pass_word = models.CharField(max_length=32, blank=True, null=True, default='')
    password_request = models.CharField(max_length=1)
    temp_password = models.CharField(max_length=200, blank=True, null=True, default='')
    phone_no = models.CharField(max_length=45, blank=True, null=True, default='')
    phone_no_alt = models.CharField(max_length=45, blank=True, null=True, default='')
    lra_member = models.CharField(max_length=45, blank=True, null=True, default='')
    address1 = models.CharField(max_length=200, blank=True, null=True, default='')
    address2 = models.CharField(max_length=200, blank=True, null=True, default='')
    city_code = models.CharField(max_length=45, blank=True, null=True, default='')
    country_code = models.CharField(max_length=45, blank=True, null=True, default='')
    contribution = models.DecimalField(max_digits=20, decimal_places=0, blank=True,)
    start_month = models.CharField(max_length=45, blank=True, null=True, default='')
    start_year = models.CharField(max_length=45, blank=True, null=True, default='')
    start_date = models.DateField(blank=True, null=True,default=now)
    status = models.CharField(max_length=1)
    terminated_date = models.DateField(blank=True, null=True,default=now)
    spouse_first_name = models.CharField(max_length=45, blank=True, null=True, default='')
    spouse_middle_name = models.CharField(max_length=45, blank=True, null=True, default='')
    spouse_last_name = models.CharField(max_length=45, blank=True, null=True, default='')
    spouse_dob = models.DateField(blank=True, null=True,default=now)
    spouse_phone = models.CharField(max_length=45, blank=True, null=True, default='')
    spouse_email = models.CharField(max_length=45, blank=True, null=True, default='')
    last_payment_date = models.DateField(blank=True, null=True,default=now)
    del_flg = models.CharField(max_length=1)
    created_by = models.CharField(max_length=45)
    created_on = models.DateTimeField(blank=True, null=True, default=now)
    last_modified_by = models.CharField(max_length=45)
    last_modified_date = models.DateTimeField(blank=True, null=True, default=now)
    total_payments = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True,)
    first_payment = models.DecimalField(max_digits=20, decimal_places=4,blank=True)
    last_payment = models.DecimalField(max_digits=20, decimal_places=4,blank=True)
    first_payment_date = models.DateField(blank=True, null=True,default=now)
    preferred_flg = models.CharField(max_length=1, blank=True, null=True, default='')
    source = models.CharField(max_length=50, blank=True, null=True, default='')
    approval_status = models.CharField(max_length=45, blank=True, null=True, default='')
    approval_date = models.DateTimeField(blank=True, null=True, default=now)
    approved_by = models.IntegerField(blank=True, null=True,)
    payment_synced = models.BooleanField(default=False)
    spouse_name = models.CharField(max_length=550,default='',blank=True)
    reference_code = models.CharField(max_length=225,default='',blank=True)
    street = models.CharField(max_length=225, default='',blank=False)
    privacy_terms_accepted = models.BooleanField(default=False)
    account_type_selected = models.BooleanField(default=False)
    call_code = models.CharField(max_length=5, blank=True, null=True, default='')
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL, blank=True,editable=False)
    full_name = models.CharField(max_length=550,default='',blank=True)
    account_type =  models.CharField(default='I',choices=(('I','Individual'), ('Cr','Corporate'), ('S','Sponsor'), ('C','Couple')), blank=True,max_length=500)
    contact_person_phone_number = models.CharField(max_length=15, default='', blank=True,verbose_name='Contact Person Number')
    contact_person_email = models.EmailField(default='',blank=True)
    contact_person_full_name = models.CharField(max_length=225,blank=True,default='')
    photo = models.ImageField(upload_to="media/partners/", blank=True)
    sector = models.CharField(max_length=225, default='',blank=True)
    street_number = models.CharField(max_length=225, default='',blank=False)

    userid = models.CharField(max_length=255, default='',blank=True,editable=False)
    tv_station = models.CharField(max_length=225, default='',blank=True)
    signup_date = models.DateField(default=now)
    profile_edit_date = models.DateField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    date_time_added = models.DateTimeField(default=now)
    secret_question = models.CharField(max_length=225,blank=True,default='')
    secret_answer = models.CharField(max_length=225,blank=True,default='')
    previous_email = models.CharField(max_length=225,blank=True,default='')
    last_token = models.CharField(max_length=225,blank=True,default='')
    profile_updated = models.BooleanField(default=False)
    suspension_count = models.IntegerField(default=0)
    briefly_suspended = models.BooleanField(default=False)
    time_suspended = models.DateTimeField(auto_now_add=False,default=now, blank=True)
    time_suspended_timestamp = models.IntegerField(default=0,blank=True)
    full_address = models.CharField(default='',blank=True,max_length=500)
    is_cgcc_member = models.BooleanField(default=False)
    contribution_frequency =  models.CharField(default='',choices=(('monthly','Monthly'), ('quarterly','Quarterly'), ('yearly','Yearly'),), blank=True,max_length=500)
    
    
    class Meta:
        managed = True
        db_table = 'dp_members'




    def __str__(self):
        return str(self.first_name) + ' ' +str(self.last_name)
       

    def save(self,*args, **kwargs):
        # self.spouse_full_name = str(self.spouse_first_name) +' ' +str(self.spouse_last_name) + ' ' +str(self.spouse_middle_name)
        if not self.first_payment:
            self.first_payment =0
        if not self.last_payment:
            self.last_payment = 0
        if self.suspension_count>2:
            self.briefly_suspended = True
            self.time_suspended =  datetime.datetime.now()
            self.time_suspended_timestamp = datetime.datetime.now().timestamp()
        secret_question=''
        for char in self.secret_question:
            if char ==  '?':
                continue
            else:
                secret_question = secret_question +char
        self.secret_question = secret_question+'?'
        self.full_address = str(self.street_number) +', '+str(self.street)+ ', ' +str(self.state)+ ', ' +str(self.country.name)
        super(DpMembers,self).save()





class EventImage(models.Model):
    image= models.ImageField(blank=False, default ='',)
    date_time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event.title



class Event(models.Model):
    content = models.CharField(max_length=20,default='event',auto_created=True)
    title = models.CharField(max_length=255, default='Event Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    start_date_time = models.DateTimeField(default=now)
    end_date_time = models.DateTimeField(default=now)
    thumbnail= models.ImageField(blank=False, default ='',)
    images=models.ManyToManyField(EventImage, blank=True, default ='',)
    video_link = models.CharField(max_length=255, default ='', blank=True, )
    full_description = HTMLField()
    date_time_added = models.DateTimeField(auto_now=True)
    eventid = models.CharField(max_length=225,default='',blank =True,)
    start_time_timestamp = models.IntegerField(default=0,blank=True)
    registration_required = models.BooleanField(default=False)
    registrations = models.ManyToManyField(DpMembers,default='',blank=True,related_name='registration')
    attendees = models.ManyToManyField(DpMembers,default='',blank=True,related_name='attendees')
    qrc = models.ImageField(blank=True, default ='',)
    read = models.ManyToManyField(DpMembers,default='',blank=True,)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if self.eventid =='':
            self.eventid= str(round(random() *1234567890))[0:5]+str(Event.objects.all().count()+1)
        self.start_time_timestamp =self.start_date_time.timestamp()
        super(Event,self).save(*args,**kwargs)


class Currency(models.Model):
    name = models.CharField(default='',max_length=10,blank=True)
    symbol = models.CharField(default='',max_length=10,blank=True)
    key = models.TextField(default='',max_length=1000,blank= True)

    def __str__(self) -> str:
        return self.name


class DpPayments(models.Model):
    months_choices = [('JAN','JAN'),('FEB','FEB'),('MAR','MAR'),('APR','APR'),('MAY','MAY'),('JUN','JUN'),('JUL','JUL'),('AUG','AUG'),('SEP','SEP'),('OCT','OCT'),('NOV','NOV'),('DEC','DEC')]
    # partner = models.ForeignKey(DpMembers,null=True,blank=True, on_delete=models.CASCADE,default='')

    pay_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0,blank=True)    
    paymentid =  models.CharField(default='',max_length=100,blank=True,)
    formatted_amount =models.CharField(default='',max_length=100,blank=True,)
    date_time_added = models.DateTimeField(auto_now=False,default=now, editable=True)
    month_covered = models.DateField(default=now)
    synced = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)
    pay_date = models.DateField(blank=True, null=True,default=now)
    payment_month = models.CharField(max_length=45, blank=True,default='')
    payment_year = models.CharField(max_length=45, blank=True, null=True, default='')

    pay_reference = HTMLField(blank=True, null=True, default='')
    description = models.CharField(max_length=2000, blank=True, null=True, default='')
    pay_source = models.CharField(max_length=45, blank=True, null=True, default='')
    del_flg = models.CharField(max_length=1)
    status = models.CharField(max_length=1, blank=True, null=True, default='')
    currency = models.CharField(max_length=3)
    applied_flg = models.CharField(max_length=1)
    member_id = models.IntegerField(blank=True,default=-1)
    member_no = models.CharField(max_length=45, blank=True, null=True, default='')
    payment_type = models.CharField(max_length=45, blank=True, null=True, default='')
    created_by = models.CharField(max_length=45, blank=True, null=True, default='')
    created_on = models.DateField(blank=True, null=True,default=now)
    last_modified_by = models.CharField(max_length=45, blank=True, null=True, default='')
    last_modified_on = models.DateField(blank=True, null=True,default=now)
    cheque_no = models.CharField(max_length=45, blank=True, null=True, default='')
    bank = models.CharField(max_length=45, blank=True, null=True, default='')
    comment = models.CharField(max_length=700, blank=True, null=True, default='')

    def __str__(self):
        return  str(self.member_id) + ' ' +str(self.payment_month) +' ' +str(self.payment_year)

    def save(self,*args, **kwargs):
        self.date_time_added = now()
        try:
            self.formatted_amount = '{:,.2f}'.format(self.amount)
        except Exception:
            pass
        super(DpPayments,self).save(*args, **kwargs)
  
    class Meta:
        managed = True
        db_table = 'dp_payments'




class Payment(models.Model):
    content_type = models.CharField(default='payment',max_length=10,blank=False,editable=False,)
    # partner = models.ForeignKey(DpMembers,default='',null=True, blank=True, on_delete=models.CASCADE)
    member_id = models.IntegerField(blank=True,default=-1)
    member_no = models.CharField(max_length=45, blank=True, null=True, default='')
    amount = models.IntegerField(default=0,blank=True)
    screenshot = models.ImageField(blank=True,default='')
    start_date = models.DateField( default=now)
    end_date = models.DateField( default=now)
    paymentid = models.CharField(max_length=100,default='',blank=True,unique=True)
    flw_ref = models.CharField(max_length=30,default='',blank=True,)
    referenceid = models.CharField(max_length=30,default='',blank=True,)
    date_time_added = models.DateTimeField(auto_now=True)
    months = models.ManyToManyField(DpPayments,default='',editable=False,blank=True)
    updated = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    formatted_amount =models.CharField(default='',max_length=100,blank=True,)
    type = models.CharField(max_length =225, choices=(('cheque','Cheque'), ('bank transfer','Bank transfer'),('online','Online'), ('pos','P.O.S')), default='',blank=False)
    comment = models.CharField(default='No Comment',max_length=500,blank=True)
    currency = models.CharField(default='',max_length=10,blank=True)
    status = models.CharField(default='status',max_length=500,blank=True)
    def __str__(self):
        return self.paymentid + ' ' +self.partner.first_name + ' '+ str(self.amount)

    def save(self,*args, **kwargs):
        super(Payment,self).save( *args, **kwargs)
        self.formatted_amount = '{:,.2f}'.format(self.amount)
        if self.paymentid == '' or Payment.objects.filter(paymentid=self.paymentid):
            TIDtemp = str(self.date_time_added)+str(round(random()*1234567890109))+str(round(random()*1234567890109))
            TID=''
            for char in range(len(TIDtemp)):
                if TIDtemp[char] == '-' or TIDtemp[char] == ':' or TIDtemp[char] == '+'or TIDtemp[char] == '.' or TIDtemp[char] == ' ':
                    continue
                else:
                    TID = TID+TIDtemp[char]
            self.paymentid= TID[0:50] +'dgp'
        super(Payment,self).save()


    # def delete(self):
    #     for monthlypayment in self.months.all():
    #         monthlypayment.delete()
    #     super(Payment,self).delete()



class Support(models.Model):
    content_type = models.CharField(default='support',max_length=10,blank=False,editable=False,)
    partner = models.ForeignKey(DpMembers,default='',null=True, blank=True, on_delete=models.CASCADE)
    supportid = models.CharField(max_length=30,default='',blank=True,unique=True)
    date_time_added = models.DateTimeField(auto_now=True)
    admin_resolved = models.BooleanField(default=False)
    partner_resolved = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    subject = models.CharField(default='No subject',max_length=100,blank=True)
    message = TextField(default='No Comment',max_length=2000,blank=True)
    resolution = TextField(default='No Comment',max_length=2000,blank=True)
    def __str__(self):
        return self.supportid

    def save(self,*args, **kwargs):
        super(Support,self).save( *args, **kwargs)
        if self.supportid == '':
             self.supportid= str(self.date_time_added.year)+str(round(random()*12345))+'0'+str(Support.objects.all().count())
        super(Support,self).save()


    def __str__(self):
        return self.subject

class TvStation(models.Model):
    content = models.CharField(max_length=20,default='tv',editable=False,auto_created=True)
    title = models.CharField(max_length=255, default='Event Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    broadcast_day = models.CharField(max_length=15, default='',choices=(('Sunday','Sunday'),('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday')))
    broadcast_time = models.TimeField(default=now)
    station_logo= models.ImageField(blank=False, default ='',)
    tv_link = models.CharField(max_length=255, default ='', blank=True, )
    date_time_added = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Announcement(models.Model):
    content = models.CharField(max_length=20,default='announcement',editable=False,auto_created=True)
    title = models.CharField(max_length=255, default='Event Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    contentid = models.CharField(max_length=225,default='',blank =True,)
    # thumbnail= models.ImageField(blank=False, default ='',)
    video_link = models.CharField(max_length=255, default ='', blank=True, )
    full_description = HTMLField()
    date_time_added = models.DateTimeField(auto_now=True)
    read = models.ManyToManyField(DpMembers,default='',blank=True,)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if self.contentid =='':
            self.contentid= str(round(random() *1234567890))[0:5]+str(Announcement.objects.all().count()+1)
        super(Announcement,self).save(*args,**kwargs)



class Video(models.Model):
    content = models.CharField(max_length=20,default='video',editable=False,auto_created=True)
    title = models.CharField(max_length=255, default='video Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    video_id = models.CharField(max_length=255, default ='', blank=True, )
    date_time_added = models.DateTimeField(auto_now=True)
    read = models.ManyToManyField(DpMembers,default='',blank=True,)

    def __str__(self):
        return self.title
    
    def save(self):
        # if 'https://' in self.link:
        #     pass

        # else:
        #     self.link = 'https://'+self.link
        super(Video, self).save()




class EventAttendees(models.Model):
    full_name =  models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length = 14,default='')
    email_address = models.EmailField()

    def __str__(self):
        return self.full_name


class ArticleImage(models.Model):
    image= models.ImageField(blank=False, default ='',)

    def __str__(self):
        return self.event.title


class Article(models.Model):
    content = models.CharField(max_length=20,default='article',editable=False,auto_created=True)
    title = models.CharField(max_length=255, default='Article Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    thumbnail= models.ImageField(blank=False, default ='',)
    images=models.ManyToManyField(ArticleImage, blank=True, default ='',)
    video_link = models.CharField(max_length=255, default ='', blank=True, )
    contentid = models.CharField(max_length=225,default='',blank =True,)
    full_description = HTMLField()
    read = models.ManyToManyField(DpMembers,default='',blank=True)
    date_time_added = models.DateTimeField(auto_now=True)
    articleid = models.CharField(max_length=20, default='',blank=True)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if self.articleid =='':
            self.articleid= str(round(random() *1234567890))[0:5]+str(Article.objects.all().count()+1)
        super(Article,self).save(*args,**kwargs)