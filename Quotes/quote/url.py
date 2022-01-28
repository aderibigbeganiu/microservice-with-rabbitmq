from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register('quotes', views.QuoteViewset, basename='quotes')
router.register('users', views.UserAPIView, basename='users')
urlpatterns = [
    path('', include(router.urls)),
]
