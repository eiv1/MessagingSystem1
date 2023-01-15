from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, UnReadMessageViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'unread-messages', UnReadMessageViewSet, basename='unread_message')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]