import phonenumbers
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField
from django_countries.serializer_fields import CountryField

from .models import SchoolOwner


class TenantOnboardingSerializer(serializers.Serializer):
    school_name = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    country = CountryField(name_only=True)
    state = serializers.CharField(max_length=100)
    default_email = serializers.EmailField()
    tenant_domain = serializers.CharField(max_length=100)
    # password = serializers.CharField(max_length=100)
    paid_until = serializers.DateField()
    phone_number = PhoneNumberField()


class TenantSerializer(serializers.ModelSerializer):
    domain_name = serializers.SerializerMethodField()

    class Meta:
        model = SchoolOwner
        fields = "__all__"

    def create(self, validated_data):
        tenant = SchoolOwner.objects.create(**validated_data)
        return tenant

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.created_on = validated_data.get("created_on", instance.created_on)
        instance.domain_url = validated_data.get("domain_url", instance.domain_url)
        instance.save()
        return instance

    def get_extra_field(self, obj):
        # This method can be used to compute the value of the extra_field
        return "Some extra value"
