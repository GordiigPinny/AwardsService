from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from Pins.models import Pin
from Pins.serializers import PinsListSerializer, PinDetailSerializer
from Pins.permissions import IsAuthenticated
from Pins.utils import get_token_from_request
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.exceptions import BaseApiRequestError


class PinListView(ListCreateAPIView):
    """
    Вьюха для возврата списка пинов
    """
    serializer_class = PinsListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, )

    def is_superuser(self, request: Request):
        try:
            return AuthRequester().is_superuser(get_token_from_request(request))[1]
        except BaseApiRequestError as e:
            # TODO: - Вот тут логи собирать
            return False

    def get_queryset(self):
        ptype = self.request.query_params.get('ptype', None)
        with_deleted = False if not self.is_superuser(self.request) \
            else self.request.query_params.get('show_deleted', False)
        if ptype is None:
            return Pin.objects.all() if with_deleted \
                else Pin.objects.filter(deleted_flg=False)
        else:
            return Pin.objects.filter(ptype=ptype) if with_deleted \
                else Pin.objects.filter(ptype=ptype, deleted_flg=False)

    def create(self, request: Request, *args, **kwargs):
        if not self.is_superuser(request):
            return Response({'error', 'Only admins can post pins'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, args, kwargs)


class PinDetailView(APIView):
    """
    Вьюха для возврата пина
    """
    permission_classes = (IsAuthenticated, )

    def is_superuser(self, request: Request):
        try:
            return AuthRequester().is_superuser(get_token_from_request(request))[1]
        except BaseApiRequestError as e:
            # TODO: - Вот тут логи собирать
            return False

    def get(self, request: Request, pk):
        with_deleted = False if not self.is_superuser(request) \
            else request.query_params.get('show_deleted', False)
        try:
            pin = Pin.objects.get(pk=pk) if with_deleted \
                else Pin.objects.get(pk=pk, deleted_flg=False)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PinDetailSerializer(instance=pin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk):
        if not self.is_superuser(request):
            return Response({'error', 'Only admin can modify pins'}, status=status.HTTP_403_FORBIDDEN)
        try:
            pin = Pin.objects.get(pk=pk, deleted_flg=False)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PinDetailSerializer(instance=pin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        if not self.is_superuser(request):
            return Response({'error', 'Only admin can modify pins'}, status=status.HTTP_403_FORBIDDEN)
        try:
            pin = Pin.objects.get(pk=pk, deleted_flg=False)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pin.deleted_flg = True
        pin.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
