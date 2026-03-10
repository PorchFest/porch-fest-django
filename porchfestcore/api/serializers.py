from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from porchfestcore.models import Porch

class PorchesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Porch
        geo_field = "coordinates"
        fields = ("name", "description", "coordinates", "performances")