from rest_framework_gis.serializers     import GeoFeatureModelSerializer
from porchfestcore.models               import Porch

class PorchMapSerializer(GeoFeatureModelSerializer):
    class Meta:
        model       = Porch
        geo_field   = "coordinates"
        fields      = ("slug", "coordinates", "performances",)