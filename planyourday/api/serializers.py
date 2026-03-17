from rest_framework         import serializers
from porchfestcore.models   import Performance, Performer, Porch

class PorchSerializer(serializers.ModelSerializer):
    class Meta:
        model       = Porch
        fields      = ("id", "name",)

class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model       = Performer
        fields      = ("id", "name", "genre")

class PerformanceSerializer(serializers.ModelSerializer):
    porch = PorchSerializer()
    performer = PerformerSerializer()
    class Meta:
        model       = Performance
        fields      = ("id", "performer", "porch", "start_time", "end_time")



