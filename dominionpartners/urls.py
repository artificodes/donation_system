"""dominionpartners URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, get_object_or_404
from general import views as gviews
from django.views.static import serve
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from general import models as gmodels
urlpatterns = [
    path('admin/v2/', admin.site.urls),
                re_path(r'',include('general.urls')),
        re_path(r'',include('partners.urls')),
        re_path(r'',include('padmin.urls')),

re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# try:
#     admin.sites.AdminSite.site_header = gmodels.General.objects.get(pk=1).platform_name
#     admin.sites.AdminSite.site_title = 'Administration'
#     admin.sites.AdminSite.index_title = gmodels.General.objects.get(pk=1).platform_name
# except ObjectDoesNotExist:
#     admin.sites.AdminSite.site_header = admin.sites.AdminSite.site_header
#     admin.sites.AdminSite.site_title = admin.sites.AdminSite.site_title
#     admin.sites.AdminSite.index_title = admin.sites.AdminSite.index_title