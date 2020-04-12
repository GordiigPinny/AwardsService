from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from Pins.models import Pin
from Pins.serializers import PinsListSerializer, PinDetailSerializer
from AwardsService.permissions import WriteOnlyBySuperuser
from ApiRequesters.Stats.decorators import collect_request_stats_decorator, CollectStatsMixin


class PinListView(ListCreateAPIView, CollectStatsMixin):
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

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PinDetailView(RetrieveUpdateDestroyAPIView, CollectStatsMixin):
    """
    Вьюха для возврата пина
    """
    permission_classes = (WriteOnlyBySuperuser, )
    serializer_class = PinDetailSerializer

    def get_queryset(self):
        with_deleted = self.request.query_params.get('with_deleted', 'False')
        with_deleted = with_deleted.lower() == 'true'
        return Pin.objects.with_deleted().all() if with_deleted else Pin.objects.all()

    @collect_request_stats_decorator()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @collect_request_stats_decorator()
    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        if response.status_code == 200:
            response.status_code = 202
        return response

    def perform_destroy(self, instance: Pin):
        instance.soft_delete()

    @collect_request_stats_decorator()
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
