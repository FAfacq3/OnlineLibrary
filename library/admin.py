from django.contrib import admin
from .models import Material, Review, DownloadLog, UserProfile

admin.site.register(Material)
admin.site.register(Review)
admin.site.register(DownloadLog)
admin.site.register(UserProfile)
