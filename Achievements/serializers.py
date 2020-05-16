from rest_framework import serializers
from Achievements.models import Achievement
from ApiRequesters.Media.MediaRequester import MediaRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class AchievementsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления ачивок
    """
    name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    descr = serializers.CharField(required=False, default='', write_only=True)
    pic_id = serializers.IntegerField(min_value=1, allow_null=False, required=False, default=1)
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Achievement
        fields = [
            'id',
            'name',
            'descr',
            'pic_id',
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
        new = Achievement.objects.create(**validated_data)
        return new


class AchievementDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор детального представления ачивки
    """
    name = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    descr = serializers.CharField(required=False, allow_blank=True, allow_null=False)
    pic_id = serializers.IntegerField(min_value=1, allow_null=False, required=False, default=1)
    deleted_flg = serializers.BooleanField(required=False)
    created_dt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Achievement
        fields = [
            'id',
            'name',
            'descr',
            'pic_id',
            'deleted_flg',
            'created_dt'
        ]

    def validate_pic_id(self, value: int):
        r = MediaRequester()
        token = get_token_from_request(self.context['request'])
        try:
            _ = r.get_image_info(value, token)
            return value
        except BaseApiRequestError:
            return 1

    def update(self, instance: Achievement, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
