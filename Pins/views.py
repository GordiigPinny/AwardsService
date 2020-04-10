from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from Pins.models import Pin
from Pins.serializers import PinsListSerializer, PinDetailSerializer
from AwardsService.permissions import WriteOnlyBySuperuser


class PinListView(ListCreateAPIView):
    """
    Вьюха для возврата списка пинов
    """
    permission_classes = (WriteOnlyBySuperuser, )
    serializer_class = PinsListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        ptype = self.request.query_params.get('ptype', None)
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        all_ = Pin.objects.all() if with_deleted else Pin.objects.with_deleted().all()
        if ptype is None:
            return all_
        else:
            return all_.filter(ptype=ptype)


class PinDetailView(RetrieveUpdateDestroyAPIView):
    """
    Вьюха для возврата пина
    """
    permission_classes = (WriteOnlyBySuperuser, )
    serializer_class = PinDetailSerializer

    def get_queryset(self):
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Pin.objects.with_deleted().all() if with_deleted else Pin.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response

    def perform_destroy(self, instance: Pin):
        instance.soft_delete()
