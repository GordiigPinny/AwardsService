from rest_framework import serializers
from Pins.models import Pin
from ApiRequesters.Media.MediaRequester import MediaRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class PinsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления пинов
    """
    name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    price = serializers.IntegerField(min_value=0, required=True)
    ptype = serializers.ChoiceField(choices=Pin.PIN_TYPE_CHOICES, required=True)
    descr = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=False, default='')
    pic_id = serializers.IntegerField(min_value=1, allow_null=False, required=False, default=1)
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Pin
        fields = [
            'id',
            'name',
            'pic_id',
            'price',
            'ptype',
            'descr',
            'deleted_flg',
        ]

    def validate_pic_id(self, value: int):
        r = MediaRequester()
        token = get_token_from_request(self.context['request'])
        try:
            _ = r.get_image_info(value, token)
            return value
        except BaseApiRequestError:
            return 1

    def create(self, validated_data):
        new = Pin.objects.create(**validated_data)
        return new


class PinDetailSerializer(serializers.ModelSerializer):
    """
    Сериалищатор детального представления пина
    """
    name = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    price = serializers.IntegerField(min_value=0, required=False)
    created_dt = serializers.DateTimeField(read_only=True)
    ptype = serializers.CharField(read_only=True)
    descr = serializers.CharField(required=False, allow_blank=True, allow_null=False)
    pic_id = serializers.IntegerField(min_value=1, allow_null=False, required=False, default=1)
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Pin
        fields = [
            'id',
            'name',
            'descr',
            'pic_id',
            'price',
            'ptype',
            'created_dt',
            'deleted_flg',
        ]

    def validate_pic_id(self, value: int):
        r = MediaRequester()
        token = get_token_from_request(self.context['request'])
        try:
            _ = r.get_image_info(value, token)
            return value
        except BaseApiRequestError:
            return 1

    def update(self, instance: Pin, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
