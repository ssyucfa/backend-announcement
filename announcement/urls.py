from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import AnnouncementViewSet

router = SimpleRouter()
router.register(r"announcement", AnnouncementViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
