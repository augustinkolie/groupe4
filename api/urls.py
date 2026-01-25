from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StationViewSet, ReadingViewSet, SensorIngestView, TriggerFetchView

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'readings', ReadingViewSet)

urlpatterns = [
    path('ingest/sensor/', SensorIngestView.as_view(), name='sensor-ingest'),
    path('ingest/trigger-fetch/', TriggerFetchView.as_view(), name='trigger-fetch'),
    path('', include(router.urls)),
]
