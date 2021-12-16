from allauth.account.forms import SignupForm
from django import forms
from partners import models as pmodels
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


class createpayment(forms.ModelForm):
    class Meta:
        model = pmodels.Payment
        fields = ('comment','end_date','start_date','referenceid','amount','type')

class createsupport(forms.ModelForm):
    class Meta:
        model = pmodels.Support
        fields = ('subject','message','resolution')


class makepayment(forms.ModelForm):
    class Meta:
        model = pmodels.Payment
        fields = ('end_date','start_date','amount')


class updatecorporateprofile(forms.ModelForm):
    class Meta:
        model = pmodels.DpMembers
        fields = ('phone_no','call_code','company_name', 'currency', 'contribution','contribution_frequency','country','city','city_code','state','street','street_number','photo','sector','contact_person_email','contact_person_phone_number','contact_person_full_name')


class changephoto(forms.ModelForm):
    class Meta:
        model = pmodels.DpMembers
        fields = ('photo',)


class updateindividualprofile(forms.ModelForm):
    class Meta:
        model = pmodels.DpMembers
        fields = ('phone_no','call_code', 'country','marital_status','gender','city','city_code','state','street','street_number','photo','contribution','contribution_frequency','currency','date_of_birth')



class updatesponsorprofile(forms.ModelForm):
    class Meta:
        model = pmodels.DpMembers
        fields = ( 'tv_station', 'phone_no','call_code','marital_status','gender', 'country','city','city_code','state','street','street_number','photo','contribution','contribution_frequency','currency','date_of_birth')



class updatecoupleprofile(forms.ModelForm):
    class Meta:
        model = pmodels.DpMembers
        fields = ('date_of_birth', 'phone_no','call_code','currency','marital_status','gender', 'contribution','contribution_frequency','country','city','city_code','state','street','street_number','photo','spouse_dob','spouse_email','spouse_phone','spouse_name')
