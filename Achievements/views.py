from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from Achievements.models import Achievement
from Achievements.serializers import AchievementsListSerializer, AchievementDetailSerializer


class AchievementsListView(ListCreateAPIView):
    """
    Вьюха для спискового представления ачивок
    """
    serializer_class = AchievementsListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        with_deleted = self.request.query_params.get('show_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Achievement.objects.with_deleted().all() if with_deleted else Achievement.objects.all()


class AchievementDetailView(RetrieveUpdateDestroyAPIView):
    """
   Вьюха для детального представления ачивки
   """
    serializer_class = AchievementDetailSerializer

    def get_queryset(self):
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Achievement.objects.with_deleted().all() if with_deleted else Achievement.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response

    def perform_destroy(self, instance: Achievement):
        instance.soft_delete()
