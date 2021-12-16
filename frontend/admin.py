from django.contrib import admin
from frontend import models as fmodels
# Register your models here.

admin.site.register(fmodels.General)
admin.site.register(fmodels.SlideShow)
admin.site.register(fmodels.CardArticle1)

admin.site.register(fmodels.Gallery)
admin.site.register(fmodels.SocialLink)
admin.site.register(fmodels.PastorsDesk)
admin.site.register(fmodels.ContactMessage)