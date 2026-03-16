from rest_framework.routers import DefaultRouter
from .views import InstitutoViewSet

router = DefaultRouter()
router.register(r'institutos', InstitutoViewSet, basename='institutos')

urlpatterns = router.urls
