from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from pets.models import SetSex


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SetSex.choices, default=SetSex.NOT_FORMED)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)