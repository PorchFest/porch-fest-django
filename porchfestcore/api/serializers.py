from rest_framework_gis.serializers     import GeoFeatureModelSerializer
from rest_framework                     import serializers
from porchfestcore.models               import Porch

class PorchMapSerializer(GeoFeatureModelSerializer):
    sponsor_logo = serializers.SerializerMethodField()

    class Meta:
        model       = Porch
        geo_field   = "coordinates"
        fields      = (
            "slug",
            "coordinates",
            "performances",
            "sponsor_logo",
            "sponsored",
            "porta_potty",
            "vendor",
            "parking",
        )
    def get_sponsor_logo(self, obj):
        if hasattr(obj, "sponsor") and obj.sponsor and obj.sponsor.map_icon:
            return obj.sponsor.map_icon.url
        if hasattr(obj, "sponsor") and obj.sponsor and obj.sponsor.logo:
            return obj.sponsor.logo.url
        return None