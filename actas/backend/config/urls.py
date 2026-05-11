from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.generic import RedirectView
from django.http import JsonResponse
from actas_app.views_dashboard import dashboard, login_page
from actas_app.dashboard_api import DashboardSummaryView

urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("login/", login_page, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("health/", lambda request: JsonResponse({"status": "ok"})),
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/actas/", include("actas_app.urls")),
    path("api/auditoria/", include("audits.urls")),
    path("api/dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard_summary"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
