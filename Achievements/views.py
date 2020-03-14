from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from Achievements.models import Achievement
from Achievements.serializers import AchievementsListSerializer, AchievementDetailSerializer
from Achievements.permissions import IsAuthenticated
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class AchievementsListView(ListCreateAPIView):
    """
    Вьюха для спискового представления ачивок
    """
    serializer_class = AchievementsListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, )

    def is_superuser(self, request: Request):
        try:
            return AuthRequester().is_superuser(get_token_from_request(request))[1]
        except BaseApiRequestError as e:
            # TODO: - Вот тут логи собирать
            return False

    def get_queryset(self):
        with_deleted = False if not self.is_superuser(self.request) \
            else self.request.query_params.get('show_deleted', False)
        return Achievement.objects.all() if with_deleted \
            else Achievement.objects.filter(deleted_flg=False)

    def create(self, request, *args, **kwargs):
        if not self.is_superuser(request):
            return Response({'error': 'Only admin can create achievements'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, args, kwargs)


class AchievementDetailView(APIView):
    """
    Вьюха для детального представления ачивки
    """
    permission_classes = (IsAuthenticated, )

    def is_superuser(self, request: Request):
        try:
            return AuthRequester().is_superuser(get_token_from_request(request))[1]
        except BaseApiRequestError as e:
            # TODO: - Вот тут логи собирать
            return False

    def get(self, request: Request, pk):
        with_deleted = self.is_superuser(request)
        try:
            ach = Achievement.objects.get(pk=pk) if with_deleted \
                else Achievement.objects.get(pk=pk, deleted_flg=False)
        except Achievement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AchievementDetailSerializer(instance=ach)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk):
        if not self.is_superuser(request):
            return Response({'error': 'Only admin can modify achievements'}, status=status.HTTP_403_FORBIDDEN)
        try:
            ach = Achievement.objects.get(pk=pk, deleted_flg=False)
        except Achievement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AchievementDetailSerializer(instance=ach, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        if not self.is_superuser(request):
            return Response({'error': 'Only admin can modify achievements'}, status=status.HTTP_403_FORBIDDEN)
        try:
            ach = Achievement.objects.get(pk=pk, deleted_flg=False)
        except Achievement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ach.deleted_flg = True
        ach.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
