from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from Pins.models import Pin
from Pins.serializers import PinsListSerializer, PinDetailSerializer


class PinListView(ListCreateAPIView):
    """
    Вьюха для возврата списка пинов
    """
    serializer_class = PinsListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = ()

    def get_queryset(self):
        ptype = self.request.query_params.get('ptype', None)
        deleted_flg = False  # TODO: - Если админ, то вытягивать из query_params
        if ptype is None:
            return Pin.objects.filter(deleted_flg=deleted_flg)
        else:
            return Pin.objects.filter(deleted_flg=deleted_flg, ptype=ptype)

    def create(self, request: Request, *args, **kwargs):
        # TODO: - Сюда на определение админа проверка
        return super().create(request, args, kwargs)


class PinDetailView(APIView):
    """
    Вьюха для возврата пина
    """
    permission_classes = ()

    def get(self, request: Request, pk):
        deleted_flg = False  # TODO: - Если админ, то вытягивать из query_params
        try:
            pin = Pin.objects.get(pk=pk, deleted_flg=deleted_flg)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PinDetailSerializer(instance=pin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk):
        # TODO: - Сюда на определение админа проверка
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
        # TODO: - Сюда на определение админа проверка
        try:
            pin = Pin.objects.get(pk=pk, deleted_flg=False)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pin.deleted_flg = True
        pin.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
