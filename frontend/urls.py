from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, get_object_or_404
from django.views.static import serve
from general import views as gviews


urlpatterns = [

    path('home/', admin.site.urls, name='admin'),
    path('', gviews.home, name='home'),
    path('pastorsdesk', gviews.pastorsdesk, name='pastors_desk'),

    path('kingdomstrategies', gviews.kingdomstrategies, name='kingdom_strategies'),
    path('contactus', gviews.contactus, name='contact_us'),
    path('slideshow', gviews.slideshow, name='slideshow'),
    path('events', gviews.events, name='events'),
    path('kingdom_strategies_home', gviews.kingdomstrategieshome,
         name='kingdom_strategies_home'),
    path('gallery_home', gviews.galleryhome, name='gallery_home'),
    path('send_message', gviews.sendmessage, name='send_message'),
    path('gallery', gviews.gallery, name='gallery'),
    path('gallery_content', gviews.gallerycontent, name='gallery_content'),
    path('moment_of_truth', gviews.momentoftruth, name='moment_of_truth'),
    path('moment_of_truth_content', gviews.momentoftruthcontent,
         name='moment_of_truth_content'),
    path('upcoming_events', gviews.upcomingevents, name='upcoming_events'),
    path('upcoming_events_content', gviews.upcomingeventscontent,
         name='upcoming_events_content'),
    path('past_events', gviews.pastevents, name='past_events'),
    path('past_events_content', gviews.pasteventscontent,
         name='past_events_content'),
    path('past_events', gviews.pastevents, name='past_events'),
    path('past_events_content', gviews.pasteventscontent,
         name='past_events_content'),
          path('videos', gviews.videos,name='videos'),
          path('videos_content', gviews.videoscontent,name='videos_content'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
