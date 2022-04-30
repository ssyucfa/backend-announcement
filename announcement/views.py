from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.response import Response

from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementDetailSerializer, BASE_FIELDS, AnnouncementCreateSerializer


class AnnouncementViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    action_serializer_classes_mapping = {
        "list": AnnouncementSerializer,
        "retrieve": AnnouncementDetailSerializer,
        "create": AnnouncementCreateSerializer,
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_date", "price"]

    def get_serializer_class(self):
        return self.action_serializer_classes_mapping.get(self.action, super().get_serializer_class())

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        if self.action == "retrieve":
            kwargs["fields"] = BASE_FIELDS + tuple(self.request.GET.get("fields", "").replace(" ", "").split(","))

        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "id": serializer.data["id"],
                "status": status.HTTP_201_CREATED,
            }, status=status.HTTP_201_CREATED, headers=headers
        )
