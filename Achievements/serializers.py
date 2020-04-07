from rest_framework import serializers
from Achievements.models import Achievement


class AchievementsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления ачивок
    """
    name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    descr = serializers.CharField(required=False, default='', write_only=True)
    pic_link = serializers.URLField(required=False, default='')
    deleted_flg = serializers.BooleanField(required=False)

    class Meta:
        model = Achievement
        fields = [
            'id',
            'name',
            'descr',
            'pic_link',
            'deleted_flg',
        ]

    def create(self, validated_data):
        new = Achievement.objects.create(**validated_data)
        return new


class AchievementDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор детального представления ачивки
    """
    name = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    descr = serializers.CharField(required=False, allow_blank=True, allow_null=False)
    pic_link = serializers.URLField(required=False, allow_blank=True, allow_null=False)
    deleted_flg = serializers.BooleanField(required=False)
    created_dt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Achievement
        fields = [
            'id',
            'name',
            'descr',
            'pic_link',
            'deleted_flg',
            'created_dt'
        ]

    def update(self, instance: Achievement, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
