from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, get_object_or_404
from django.views.static import serve
from partners import views as pviews
from general import views as gviews


urlpatterns = [
    path('', pviews.dashboard, name='partner_dashboard'),
    path('partner', pviews.dashboard, name='partner_dashboard'),
    path('fixdb', pviews.fixdb, name='fixdb'),
    path('partner/allpayments', pviews.allpayments, name='all_payments'),
    path('partner/dashboard', pviews.dashboard, name='partner_dashboard'),
    path('partner/dashboardcontent', pviews.dashboardcontent, name='partner_dashboard_content'),
    path('partner/eventregistration/<str:eventid>',
         pviews.eventregistration, name='partner_event_registration'),
    path('partner/eventdetails/<str:eventid>', pviews.eventdetails, name='partner_event_details'),
    path('partner/information_desk_content/<str:content>/<str:cid>',
         pviews.informationdeskcontent, name='partner_information_desk_content'),
    path('partner/select_account_type/', pviews.select_account_type, name='partner_select_account_type'),
    path('partner/confirmemail', pviews.confirmemail, name='partner_confirm_email'),
    path('partner/confirmemailpage/', pviews.confirmemailpage, name='partner_confirm_email_page'),
    path('partner/recent_remittances/<str:userid>', pviews.recentremittances, name='partner_recent_remittances'),
    path('partner/all_payments/<str:userid>', pviews.allpayments, name='partner_all_payments'),
    path('partner/change_photo', pviews.changephoto, name='partner_change_photo'),

    path('partner/verifyevent', pviews.verifyevent, name='partner_verify_event'),
    path('partner/profile', pviews.myprofile, name='partner_my_profile'),
    path('partner/announcements', pviews.announcements, name='partner_announcements'),
    path('partner/support/change_status/<str:status>/<str:supportid>', pviews.changesupportstatus, name='partner_change_support_status'),

    path('partner/announcement/<str:announcementid>',
         pviews.announcementdetails, name='partner_announcement_details'),
    path('partner/support/details/<str:supportid>',
         pviews.supportdetails, name='partner_support_details'),
    path('partner/support', pviews.support, name='partner_support'),
    path('partner/support/create', pviews.createsupport, name='partner_create_support'),
    path('partner/articles', pviews.articles, name='partner_articles'),
    path('partner/article/<str:articleid>',
         pviews.articledetails, name='partner_article_details'),    
        path('partner/videos', pviews.videos, name='partner_videos'),
    path('partner/mypayments', pviews.mypayments, name='partner_my_payments'),
    path('partner/createpayment/<str:action>', pviews.createpayment, name='partner_create_payment'),
    path('partner/makepayment', pviews.makepayment, name='partner_make_payment'),
    path('partner/recordpayment', pviews.recordpayment, name='partner_record_payment'),
    path('partner/updatepayment/<str:paymentid>', pviews.updatepayment, name='partner_update_payment'),
    path('partner/cancelpayment/<str:paymentid>', pviews.cancelpayment, name='partner_cancel_payment'),

    path('partner/get_currency_key', pviews.getcurrencykey, name='get_currency_key'),
    path('partner/events', pviews.events, name='partner_events'),

    path('partner/update_profile/', pviews.updateprofile, name='partner_update_profile'),

    path("accounts/signup/", gviews.signup, name='partner_account_signup'),
    url("accounts/login/", gviews.loginuser, name='partner_account_login'),
    url("accounts/logout/", gviews.logoutuser, name='partner_account_logout'),

    url(r'^account_activation_sent/$', gviews.account_activation_sent,
        name='partner_account_activation_sent'),
    url(r'^accounts/', include('allauth.urls')),
    url('partner/activate-account', gviews.activate, name='partner_activate_account'),
    url('partner/resendactivationcode', gviews.resendactivationcode,
        name='partner_resend_activation_code'),
    url('partner/unsuspend', gviews.unsuspend, name='partner_unsuspend'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
