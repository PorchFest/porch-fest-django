from rest_framework_gis.serializers     import (
    GeoFeatureModelSerializer,
    GeoFeatureModelListSerializer
)
from rest_framework                     import serializers
from src.apps.porchfest.models               import Porch


class FeatureCollectionListSerializer(GeoFeatureModelListSerializer):
    def to_representation(self, data):
        collection = super().to_representation(data)

        collection["count"] = len(collection["features"])
        return collection


class PorchMapSerializer(GeoFeatureModelSerializer):
    sponsor_logo = serializers.SerializerMethodField()

    class Meta:
        model = Porch
        geo_field = "coordinates"
        list_serializer_class = FeatureCollectionListSerializer
        fields = (
            "slug",
            "coordinates",
            "performances",
            "sponsor_logo",
            "sponsored",
            "porta_potty",
            "vendor",
            "parking",
            "info_booth",
            "drinking_water",
            "bicycle_repair",
            "after_party",
            "childrens_activities",
        )

    def get_sponsor_logo(self, obj):
        if hasattr(obj, "sponsor") and obj.sponsor and obj.sponsor.map_icon:
            return obj.sponsor.map_icon.url
        if hasattr(obj, "sponsor") and obj.sponsor and obj.sponsor.logo:
            return obj.sponsor.logo.url
        return None