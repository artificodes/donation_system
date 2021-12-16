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
from padmin import views as aviews

urlpatterns = [
    path('admin/', aviews.dashboard, name='admin_dashboard'),

    path('admin/dashboard', aviews.dashboard, name='admin_dashboard'),
    path('admin/regularize_payments', aviews.regularizepayments, name='admin_regularize_payments'),
    path('admin/all_partners', aviews.allpartners, name='admin_all_partners'),
    path('admin/dashboardcontent', aviews.dashboardcontent, name='admin_dashboard_content'),
    path('admin/eventregistration/<str:eventid>',
         pviews.eventregistration, name='admin_event_registration'),
    path('admin/eventdetails/<str:eventid>', pviews.eventdetails, name='admin_event_details'),
    path('admin/information_desk_content/<str:content>/<str:cid>',
         pviews.informationdeskcontent, name='admin_information_desk_content'),

    path('admin/verifyevent', pviews.verifyevent, name='admin_verify_event'),
    path('admin/memberprofile/<str:userid>', aviews.memberprofile, name='admin_member_profile'),

    path('admin/profile', pviews.myprofile, name='admin_profile'),
    path('admin/announcements', pviews.announcements, name='admin_announcements'),
    path('admin/announcement/<str:announcementid>',
         pviews.announcementdetails, name='admin_announcement_details'),
    path('admin/videos', pviews.videos, name='admin_videos'),
    path('admin/payments', aviews.payments, name='admin_payments'),
    path('admin/payments/search', aviews.searchpayment, name='admin_payment_search'),
    path('admin/payments/sort/dates', aviews.sortpaymentsfromdate, name='admin_sort_payments_from_dates'),
    path('admin/payments/sort/download', aviews.sortedpaymenttofile, name='admin_download_payments'),
    path('admin/send_message', aviews.sendmessage, name='admin_send_message'),
    path('admin/members/search', aviews.membersearch, name='admin_member_search'),
    path('admin/recent_remittances/<str:userid>', aviews.recentremittances, name='admin_partner_recent_remittances'),
    path('admin/dashboard/members_analysis', aviews.members_analysis, name='admin_members_analysis'),
    path('admin/dashboard/members_payments_analysis/<str:userid>', aviews.members_payment_analysis, name='admin_members_payments_analysis'),
    path('admin/information_desk_content/<str:content>/<str:cid>',
         aviews.informationdeskcontent, name='admin_information_desk_content'),
    path('admin/record_payment/<str:userid>', aviews.recordpayment, name='admin_record_payment'),
    path('admin/filtered_members/send_message', aviews.messagefilteredmembers, name='admin_message_filtered_members'),
    path('admin/filtered_members', aviews.filteredmembers, name='admin_filtered_members'),
    path('admin/filtered_members/download', aviews.filteredmembersdownload, name='admin_download_filtered_members'),
    path('admin/payments/sort/<str:param>', aviews.sortpayments, name='admin_sort_payments'),
    path('admin/allmembers', aviews.members, name='admin_all_members'),
    path('admin/updatepayment/<str:paymentid>', pviews.updatepayment, name='admin_update_payment'),
    path('admin/select_account_type', pviews.select_account_type, name='admin_select_account_type'),
    path('admin/member_signup', aviews.adminmembercreation, name='admin_member_signup'),
    path('admin/support/reply/<str:supportid>', aviews.replysupport, name='admin_reply_support'),
    path('admin/supports', aviews.supports, name='admin_support'),

    path('admin/events', pviews.events, name='admin_events'),
    path('admin/create_payment/<str:action>', aviews.createpayment, name='admin_create_payment'),
    path('admin/select_account_type/<str:userid>', aviews.adminselectaccounttype, name='admin_select_account_type'),
    path('admin/partner_page/<str:userid>', aviews.memberpage, name='admin_member_page'),
    path('admin/partner/all_payments/<str:userid>', aviews.partnersallpayments, name='admin_partner_all_payments'),
    path('admin/all_payments/', aviews.allpayments, name='admin_all_payments'),
    path('admin/recent_payments/', aviews.recentremittances, name='admin_recent_payments'),
    path('admin/make_payment/<str:userid>', aviews.makepayment, name='admin_make_payment'),
    path('admin/create_payment/lite/<str:userid>', aviews.createpaymentlite, name='admin_create_payment_lite'),

    path('admin/update_member_profile/<str:userid>', aviews.updatememberprofile, name='admin_update_member_profile'),

    path("accounts/signup/", gviews.signup, name='admin_account_signup'),
    # url("accounts/login/", aviews.loginuser, name='admin_account_login'),
    url("accounts/logout/", gviews.logoutuser, name='admin_account_logout'),

    url(r'^account_activation_sent/$', gviews.account_activation_sent,
        name='admin_account_activation_sent'),
    url(r'^accounts/', include('allauth.urls')),
    url('admin/activate-account', gviews.activate, name='admin_activate_account'),
    url('admin/resendactivationcode', gviews.resendactivationcode,
        name='admin_resend_activation_code'),
    url('admin/unsuspend', gviews.unsuspend, name='admin_unsuspend'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
