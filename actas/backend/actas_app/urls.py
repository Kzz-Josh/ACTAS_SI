from rest_framework.routers import DefaultRouter

from .views import (
    ActaNacimientoViewSet,
    ActaMatrimonioViewSet,
    ActaDefuncionViewSet,
)

router = DefaultRouter()
router.register(r"nacimientos", ActaNacimientoViewSet, basename="actas-nacimientos")
router.register(r"matrimonios", ActaMatrimonioViewSet, basename="actas-matrimonios")
router.register(r"defunciones", ActaDefuncionViewSet, basename="actas-defunciones")

urlpatterns = router.urls
