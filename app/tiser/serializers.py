from rest_framework import serializers

from .models import Category, Tiser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TiserSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Tiser
        fields = "__all__"

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        tiser = Tiser.objects.create(**validated_data)

        return tiser


class TiserListSerializer(serializers.Serializer):
    tisers = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=100
    )


class TiserListPaymentSerializer(TiserListSerializer):
    price = serializers.FloatField(min_value=0.01)


class TiserPaymentResponceSerializer(serializers.Serializer):
    message = serializers.CharField()
    count = serializers.IntegerField()
