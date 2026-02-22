from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from ..models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)
from ..filtersets import (
    WavelengthGridFilterSet,
    WavelengthChannelFilterSet,
    OpticalCircuitFilterSet,
    OpticalCircuitHopFilterSet,
    MultiplexGroupFilterSet,
    MultiplexGroupMemberFilterSet,
)
from .serializers import (
    WavelengthGridSerializer,
    WavelengthChannelSerializer,
    OpticalCircuitSerializer,
    OpticalCircuitHopSerializer,
    MultiplexGroupSerializer,
    MultiplexGroupMemberSerializer,
)


class WavelengthGridViewSet(NetBoxModelViewSet):
    queryset = WavelengthGrid.objects.annotate(channel_count=Count('channels'))
    serializer_class = WavelengthGridSerializer
    filterset_class = WavelengthGridFilterSet


class WavelengthChannelViewSet(NetBoxModelViewSet):
    queryset = WavelengthChannel.objects.all()
    serializer_class = WavelengthChannelSerializer
    filterset_class = WavelengthChannelFilterSet


class OpticalCircuitViewSet(NetBoxModelViewSet):
    queryset = OpticalCircuit.objects.annotate(hop_count=Count('hops'))
    serializer_class = OpticalCircuitSerializer
    filterset_class = OpticalCircuitFilterSet


class OpticalCircuitHopViewSet(NetBoxModelViewSet):
    queryset = OpticalCircuitHop.objects.all()
    serializer_class = OpticalCircuitHopSerializer
    filterset_class = OpticalCircuitHopFilterSet


class MultiplexGroupViewSet(NetBoxModelViewSet):
    queryset = MultiplexGroup.objects.annotate(member_count=Count('members'))
    serializer_class = MultiplexGroupSerializer
    filterset_class = MultiplexGroupFilterSet


class MultiplexGroupMemberViewSet(NetBoxModelViewSet):
    queryset = MultiplexGroupMember.objects.all()
    serializer_class = MultiplexGroupMemberSerializer
    filterset_class = MultiplexGroupMemberFilterSet
