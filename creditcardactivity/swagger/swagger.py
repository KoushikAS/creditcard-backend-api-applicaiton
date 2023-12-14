from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Demo Credit Card Application",
        default_version="v1",
        description="A demonstration application for Pomelo coding test implemented by Koushik Annareddy Sreenath. See detailed requirements [GitHub Gist](https://gist.github.com/aseemk/89aaa72d4d60c5448307250ca0179f5c).",
        contact=openapi.Contact(email="koushik.annareddysreenath@duke.com"),
    ),
    public=True,
    permission_classes=(),
)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
