from django_hosts import patterns, host
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'app', 'partners.urls', name='partners'),
    host(r'user', 'user.urls', name='user'),
        host(r'admin', 'padmin.urls', name='admin'),

)