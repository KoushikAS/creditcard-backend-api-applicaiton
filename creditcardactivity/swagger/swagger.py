from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Pomelo Demo APP",
        default_version="v1",
        description="Demo app for showcasing the pomelo app",
        contact=openapi.Contact(email="KoushikAnnareddySreenath@duke.com"),
    ),
    public=True,
    permission_classes=(),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]