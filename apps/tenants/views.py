from django.conf import settings
from django.contrib.auth import get_user_model
from django_tenants.utils import get_tenant_model, schema_context
from rest_framework import status, response, views, permissions
from apps.school.models import School
from apps.tenants.models import Domain, SchoolOwner

from apps.tenants.serializers import TenantCreateSerializer, TenantSerializer

from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()
TenantModel = get_tenant_model()


class TenantCreateView(views.APIView):
    serializer_class = TenantCreateSerializer
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.TokenAuthentication]

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        serializer = TenantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data from the serializer
        name = serializer.validated_data.get(
            "name",
        )
        domain_url = serializer.validated_data.get("tenant_domain")
        country = serializer.validated_data.get("country")
        state = serializer.validated_data.get("state")
        default_email = serializer.validated_data.get("default_email")
        phone_number = serializer.validated_data.get("phone_number")

        # create your public tenant
        tenant = SchoolOwner(
            schema_name=name,
            name=name.lower(),
            email=default_email,
            country=str(country),
            state=state,
            phone_number=phone_number,
        )
        tenant.save()

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = (
            domain_url.lower()
        )  # don't add your port or www here! on a local server you'll want to use localhost here
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

        # Perform any additional operations required for creating the tenant and domain
        # with schema_context(tenant):
        #     # Create the superuser for the tenant
        #     user = User.objects.create_user(
        #         email='ola@mail.com',
        #         password=settings.ADMIN_PASSWORD,
        #         phone_number=phone_number,
        #     )
        #     user.is_superuser = True
        #     user.is_staff = True
        #     user.user_type = 6
        #     user.save()
        #     school = School.objects.create(
        #         admin=user,
        #         name=name,
        #         domain_name=domain_name,
        #     )
        #     school.save()
        # # Switch back to the default schema
        # connection.set_schema_to_public()

        return response.Response(
            {
                "success": f"{tenant.schema_name} Tenant and {domain.domain} domain created successfully."
            },
            status=status.HTTP_201_CREATED,
        )


tenant_create = TenantCreateView.as_view()
