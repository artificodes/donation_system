from datetime import date, datetime
from socket import socket
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# from padmin.views import birthday
from partners import models as pmodels
from general import models as gmodels
from partners.email_sender import sendBirthday,sendMonthly,sendSheduled
from padmin import models as amodels

def birthday():
    partners = pmodels.DpMembers.objects.filter(date_of_birth__month = datetime.today().month,date_of_birth__day=datetime.today().day).exclude(del_flg='Y')
    for partner in partners:
        if partner.email_addres and partner.first_name.lower() == 'chinecherem':
            subject = 'Happy Birthday - Dominion Partners Global'
         

            message = render_to_string('padmin/happy_birthday.html', {
                    'name': partner.first_name,
                    'date':datetime.today().date(),
                    'title':'HAPPY BIRTHDAY!!!',
                    'socials':gmodels.SocialLink.objects.all()
                })
            recipient_list = [partner.email_addres, ]

            sendBirthday(recipient_list,message,message,subject)

            # try:
            #     send_mail( subject, message, email_from, recipient_list,html_message=message )
            # except socket.gaierror:
            #     pass

def greetmonthly():
    partners = pmodels.DpMembers.objects.all().exclude(del_flg='Y')
    recipient_list = []
    for partner in partners:
        try:
            if partner.email == 'anyaoha' and partner.first_name.lower() == 'chinecherem':
                recipient_list.append(partner.email_addres)
            else:
                print(partner.first_name,partner.pk)


        except Exception:
            print(partner.first_name,partner.pk)
    subject = 'Thank you - Dominion Partners Global'


    message = render_to_string('padmin/monthly_greeting.html', {
            'name': partner.first_name,
            'date':datetime.today().date(),
            'title':'THANK YOU',
            'socials':gmodels.SocialLink.objects.all()
        })

    sendMonthly(recipient_list,message,message,subject)



def sendPersonalizedEmail(email,recipient_list,user):
    message = render_to_string('padmin/personalized_sheduled_email.html', {
            'user':user,
            'body':email.body,
            'date':datetime.today().date(),
            'title':email.subject,
            'socials':gmodels.SocialLink.objects.all(),
            'email':email
        })
    # print('Weekly')

    sendSheduled(recipient_list,message,message,email.subject,email.pk)



def sendBroadcastEmail(email,recipient_list):
    message = render_to_string('padmin/sheduled_email.html', {
            
            'body':email.body,
            'date':datetime.today().date(),
            'title':email.subject,
            'socials':gmodels.SocialLink.objects.all(),
            'email':email
        })
    # print('Weekly')

    sendSheduled(recipient_list,message,message,email.subject,email.pk)




def sendsheduleemails():
    emails = amodels.SheduledEmail.objects.filter(end__gte=datetime.today().date(),start__lte=datetime.today().date())
    if emails:
        recipient_list = []

        partners = pmodels.DpMembers.objects.all().exclude(del_flg='Y')
        for email in emails:
            d0 = date(email.last_sent.date().year, email.last_sent.date().month, email.last_sent.date().day)
            d1 = datetime.today().date()
            days = (d1 - d0).days
            print(days)
            if email.personalized:
                for partner in partners:
                    recipient_list = []
                    try:
                        if partner.last_name.lower() == 'anyaoha' and partner.first_name.lower() == 'chinecherem':
                            recipient_list.append(partner.email_addres)
                            if email.days != 'all' and int(email.days) != datetime.today().weekday():
                                continue
                            else:
                                frequency = email.frequency
                                if frequency != 'daily':
                                    if frequency == 'weekly' and days == 7:
                                        # sendPersonalizedEmail(email,['ogohifeoma@yahoo.com','kamsipearl@gmail.com','s.bakare@thecitadelglobal.org','tg@thecitadelglobal.org', 'c.anyaoha@thecitadelglobal.org'],partner.first_name)
                                        sendPersonalizedEmail(email,recipient_list,partner.first_name)
                                    elif frequency == 'monthly' and days >= 28:
                                        sendPersonalizedEmail(email,recipient_list,partner.first_name)

                                else:
                                        sendPersonalizedEmail(email,recipient_list,partner.first_name)
                        else:
                            print(partner.first_name,partner.pk)


                    except Exception:
                        print(partner.first_name,partner.pk)


            else:
                for partner in partners:
                    try:
                        if partner.last_name.lower() == 'anyaoha' and partner.first_name.lower() == 'chinecherem':
                            recipient_list.append(partner.email_addres)
                        else:
                            print(partner.first_name,partner.pk)


                    except Exception:
                        print(partner.first_name,partner.pk)
                if email.days != 'all' and int(email.days) != datetime.today().weekday():
                    continue
                else:
                    frequency = email.frequency
                    if frequency != 'daily':
                        if frequency == 'weekly' and days == 7:
                            sendBroadcastEmail(email,recipient_list)
                        elif frequency == 'monthly' and days >= 28:
                            sendBroadcastEmail(email,recipient_list)

                    else:
                            sendBroadcastEmail(email,recipient_list)

    else:
        print('No Email for today')


def happybirthday():
    scheduler = BackgroundScheduler()
    scheduler.add_job(birthday, 'interval', minutes=0.2)
    scheduler.start()

def greet():
    scheduler = BackgroundScheduler()
    scheduler.add_job(greetmonthly, 'interval', minutes=0.5)
    scheduler.start()


def customsheduled():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sendsheduleemails, 'interval', minutes=1)
    scheduler.start()