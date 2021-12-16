from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
# from clients import models as cmodels
from django.core.exceptions import ObjectDoesNotExist
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # customuser = cmodels.Client.objects.get(user=user)
        return (
           
            # six.text_type(user.pk) + six.text_type(timestamp) +
            # six.text_type(customuser.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()