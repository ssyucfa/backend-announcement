from django.contrib import admin

from .models import Announcement, Image


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
