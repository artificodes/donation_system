from django.contrib import admin
from partners import models as pmodels

admin.site.register(pmodels.Support)
admin.site.register(pmodels.DpPayments)

admin.site.register(pmodels.DpMembers)
admin.site.register(pmodels.VisitorsLog)
admin.site.register(pmodels.Event)
admin.site.register(pmodels.EventImage)
admin.site.register(pmodels.Announcement)
admin.site.register(pmodels.Article)
admin.site.register(pmodels.ArticleImage)
admin.site.register(pmodels.Video)
admin.site.register(pmodels.TvStation)
admin.site.register(pmodels.Payment)
admin.site.register(pmodels.Currency)
