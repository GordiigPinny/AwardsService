from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from Achievements.models import Achievement
from Achievements.serializers import AchievementsListSerializer, AchievementDetailSerializer
from AwardsService.permissions import WriteOnlyBySuperuser
from ApiRequesters.Stats.decorators import collect_request_stats_decorator, CollectStatsMixin


class AchievementsListView(ListCreateAPIView, CollectStatsMixin):
    """
    Вьюха для спискового представления ачивок
    """
    permission_classes = (WriteOnlyBySuperuser, )
    serializer_class = AchievementsListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Achievement.objects.with_deleted().all() if with_deleted else Achievement.objects.all()

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AchievementDetailView(RetrieveUpdateDestroyAPIView, CollectStatsMixin):
    """
    Вьюха для детального представления ачивки
    """
    permission_classes = (WriteOnlyBySuperuser,)
    serializer_class = AchievementDetailSerializer

    def get_queryset(self):
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Achievement.objects.with_deleted().all() if with_deleted else Achievement.objects.all()

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response

    def perform_destroy(self, instance: Achievement):
        instance.soft_delete()

    @collect_request_stats_decorator()
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
