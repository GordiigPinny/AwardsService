from rest_framework import serializers
from Pins.models import Pin


class PinsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления пинов
    """
    descr = serializers.CharField(write_only=True, required=False)
    pin_pic_link = serializers.URLField(required=False)
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Pin
        fields = [
            'id',
            'name',
            'pin_pic_link',
            'price',
            'ptype',
            'descr',
            'deleted_flg',
        ]

    def create(self, validated_data):
        new = Pin.objects.create(**validated_data)
        return new


class PinDetailSerializer(serializers.ModelSerializer):
    """
    Сериалищатор детального представления пина
    """
    created_dt = serializers.DateTimeField(read_only=True)
    ptype = serializers.CharField(read_only=True)
    descr = serializers.CharField(required=False)
    pin_pic_link = serializers.URLField(required=False)
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Pin
        fields = [
            'id',
            'name',
            'descr',
            'pin_pic_link',
            'price',
            'ptype',
            'created_dt',
            'deleted_flg',
        ]

    def update(self, instance: Pin, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
