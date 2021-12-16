from email.policy import default
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import (
    get_available_image_extensions,
    FileExtensionValidator,
)
from django.utils.timezone import now

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
from django.core.exceptions import ValidationError

class General(models.Model):
    platform_name = models.CharField(max_length=255, default='Business Name')
    church_name_prefix = models.CharField(max_length=255, default='Business Name Prefix')
    logo= models.ImageField(blank=False, default ='',)
    full_logo= models.ImageField(blank=False, default ='',)
    background_image= models.ImageField(default ='',blank=True)
    error_404_background= models.ImageField(default ='',blank=True)
    error_500_background= models.ImageField(default ='',blank=True)
    logo_icon= models.ImageField(default ='',blank=True)
    phone_number_1 = models.CharField(max_length=13, default ='', blank=True, )
    phone_number_2 = models.CharField(max_length=13, default ='', blank=True, )
    address = models.CharField(max_length=1000, default ='', blank=True, )
    email = models.CharField(max_length=255, default ='', blank=True, )

    def __str__(self):
        return self.platform_name
    class Meta:
        verbose_name ='Setting'

    def clean(self):
        """
        Throw ValidationError if you try to save more than one model instance
        See: http://stackoverflow.com/a/6436008
        """
        model = self.__class__
        if (model.objects.count() > 0 and
                self.id != model.objects.get().id):
            raise ValidationError(
                "Can only create 1 instance of %s." % model.__name__)


class SlideShow(models.Model):
    name = models.CharField(max_length=255, default='Slide show name')
    description = models.CharField(max_length=1000, default='Description',blank = True)
    mobile_image= models.ImageField(blank=False, default ='',)
    desktop_image= models.ImageField(blank=False, default ='',)
    link = models.CharField(max_length=255, default ='', blank=True, )
    transition_type = models.CharField(max_length=255, choices=(('uk-transform-origin-center-left','origin to center left'),
    ('uk-transform-origin-center-right','origin to center right'),('uk-transform-origin-center','origin to center'),
    ('no-transition','None')), default='None')
    kenburns = models.BooleanField(default=False,verbose_name='Use kenburns effect')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name ='Slideshow'




class CardArticle1(models.Model):
    title = models.CharField(max_length=255, default='Article Title')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    image= models.ImageField(blank=False, default ='',)
    link = models.CharField(max_length=255, default ='', blank=True, )
    full_description = HTMLField()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image= models.ImageField(blank=False, default ='',)
    title = models.CharField(max_length=255, default='Image Title')
    date_time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PastorsDesk(models.Model):
    title = models.CharField(max_length=255, default='Pastors Desk')
    short_description = models.CharField(max_length=1000, default='short description',blank = True)
    thumbnail= models.ImageField(blank=False, default ='',)
    video_link = models.CharField(max_length=255, default ='', blank=True, )
    full_description = HTMLField()
    date_time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        """
        Throw ValidationError if you try to save more than one model instance
        See: http://stackoverflow.com/a/6436008
        """
        model = self.__class__
        if (model.objects.count() > 0 and
                self.id != model.objects.get().id):
            raise ValidationError(
                "Can only create 1 instance of %s." % model.__name__)

class SocialLink(models.Model):
    name = models.CharField(max_length=255, default='Event Title')
    color = models.CharField(max_length=1000, default='short description',blank = True)
    link = models.CharField(max_length=255, default ='', blank=True, )
    date_time_added = models.DateTimeField(auto_now=True)
    image= models.ImageField(blank=False, default ='',)
    def __str__(self):
        return self.name

    def save(self):
        if 'https://' in self.link:
            pass

        else:
            self.link = 'https://'+self.link
        super(SocialLink,self).save()


class BirthdayImages(models.Model):
    name = models.CharField(max_length=255, default='Attachment')
    date_time_added = models.DateTimeField(auto_now=True)
    image= models.ImageField(blank=False, default ='',)
    def __str__(self):
        return self.name

    # def save(self):
    #     if 'https://' in self.link:
    #         pass

    #     else:
    #         self.link = 'https://'+self.link
    #     super(SocialLink,self).save()



class ContactMessage(models.Model):
    name = models.CharField(max_length=255, default='Senders name')
    message = HTMLField()
    number = models.CharField(max_length=255, default='Senders name')
    email = models.EmailField(default='')
    date_time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name