from django.db import models


class Image(models.Model):
    photo = models.ImageField()
    announcement = models.ForeignKey("Announcement", on_delete=models.CASCADE, related_name="images")


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
