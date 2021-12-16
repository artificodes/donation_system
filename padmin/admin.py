from django.contrib import admin
from  padmin import models as amodels



admin.site.register(amodels.Attachment)
admin.site.register(amodels.SheduledEmail)
