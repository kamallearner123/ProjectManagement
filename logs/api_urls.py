from rest_framework.routers import DefaultRouter
from .api_views import DailyLogViewSet

router = DefaultRouter()
router.register(r'logs', DailyLogViewSet)

urlpatterns = router.urls