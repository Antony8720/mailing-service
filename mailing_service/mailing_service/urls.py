from api.views import ClientViewSet, MailingViewSet, MessageViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .yasg import swaggerurlpatterns

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
urlpatterns += swaggerurlpatterns
