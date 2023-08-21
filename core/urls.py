from django.contrib import admin
from django.urls import include, path, re_path

# from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School Management System Backend API",
        default_version="v1",
        description="This API contains all the endpoints and the base of our operations",
        terms_of_service="https://www.saascrafters.com/terms/",
        contact=openapi.Contact(email="contact@saascrafters.com"),
        license=openapi.License(name="SaaS Crafters Official License"),
    ),
    public=True,
)

urlpatterns = [
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # path('api/docs/', include_docs_urls(title='Invoice API Documentation')),  # Custom API documentation
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/", include("apps.user.urls", namespace="accounts")),
    # path("api/v1/profiles", include("apps.profiles.urls", namespace="profiles")),
    # path("api/v1/customers", include("apps.customers.urls", namespace="customers")),
    # path("api/v1/invoice", include("apps.invoice.urls", namespace="invoice")),
    # path("api/v1/records", include("apps.records.urls", namespace="records")),
    path("admin/", admin.site.urls),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair_view"),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_obtain_refresh_view",
    ),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.authtoken")),
]
