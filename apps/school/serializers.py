from rest_framework import serializers

from .models import School, SchoolArms, SchoolBreak, SchoolContact


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class SchoolContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolContact
        fields = "__all__"
