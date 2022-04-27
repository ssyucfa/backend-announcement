from django.conf import settings
from rest_framework import serializers

from .models import Announcement, Image


BASE_FIELDS = ("title", "price", "image")


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("photo", )


class AnnouncementSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Announcement
        fields = BASE_FIELDS

    def to_representation(self, instance: Announcement) -> dict[str, any]:
        representation = super().to_representation(instance)
        image = instance.images.first()
        if image:
            representation["image"] = settings.SITE_URL + image.photo.url
        return representation


class AnnouncementDetailSerializer(DynamicFieldsModelSerializer, AnnouncementSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Announcement
        fields = BASE_FIELDS + ("description", "images")


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Announcement
        fields = ("id", "title", "price", "description", "images")

    def create(self, validated_data: dict[str, any]):
        images = validated_data.pop("images")
        announcement = Announcement.objects.create(**validated_data)
        for image in images[:3]:
            Image.objects.create(announcement=announcement, photo=image.photo)
        return announcement
