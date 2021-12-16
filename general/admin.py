from django.contrib import admin
from general import models as gmodels

admin.site.register(gmodels.General)
admin.site.register(gmodels.SlideShow)
admin.site.register(gmodels.CardArticle1)

admin.site.register(gmodels.Gallery)
admin.site.register(gmodels.SocialLink)
admin.site.register(gmodels.PastorsDesk)
admin.site.register(gmodels.ContactMessage)
admin.site.register(gmodels.BirthdayImages)