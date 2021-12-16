from email.policy import default
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
from random import choices, random
from tinymce.models import HTMLField
import os
import base64
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# from users import models as cmodels
from general import models as gmodels
from django.utils.timezone import now



class Attachment(models.Model):
    name = models.CharField(default='',blank=False,max_length=50)
    file= models.FileField(blank=False, default ='',)
    date_time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class SheduledEmail(models.Model):
    subject = models.CharField(default=" ",blank=True,max_length=50, verbose_name='Email Subject')
    attachments = models.ManyToManyField(Attachment)
    body_image = models.ImageField(default='',blank=True)
    image_position = models.CharField(default='',max_length=50, blank=True,choices=(('top','top'),('bottom','bottom')))
    body = HTMLField(blank=False,verbose_name='Email body')
    start = models.DateTimeField(default=now(),blank=False,verbose_name='When should this email start broadcasting?')
    end = models.DateTimeField(default=now(),blank=False,verbose_name='When should this email stop broadcasting?')
    frequency = models.CharField(default='',max_length=50, blank=True,choices=(('daily','daily'),('weekly','weekly'),('monthly','monthly')))
    days = models.CharField(default='', max_length=50, blank=True,choices=(('all','All'),('0','Mondays'),('1','Tuesdays'),('2','Wednesdays'),('3','Thursdays'),('4','Fridays'),('5','Saturdays'),('6','Sundays')))
    last_sent = models.DateTimeField(default=now,blank=True)
    date_time_added = models.DateTimeField(auto_now=True)
    personalized = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.subject
