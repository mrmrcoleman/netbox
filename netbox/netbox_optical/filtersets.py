import django_filters
from django.utils.translation import gettext_lazy as _

from dcim.models import Device, Interface
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Tenant

from .models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)


class WavelengthGridFilterSet(NetBoxModelFilterSet):
    grid_type = django_filters.CharFilter()

    class Meta:
        model = WavelengthGrid
        fields = ('id', 'name', 'grid_type')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class WavelengthChannelFilterSet(NetBoxModelFilterSet):
    grid_id = django_filters.ModelMultipleChoiceFilter(
        queryset=WavelengthGrid.objects.all(),
        field_name='grid',
        label=_('Grid'),
    )

    class Meta:
        model = WavelengthChannel
        fields = ('id', 'name', 'grid')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class OpticalCircuitFilterSet(NetBoxModelFilterSet):
    status = django_filters.CharFilter()
    channel_id = django_filters.ModelMultipleChoiceFilter(
        queryset=WavelengthChannel.objects.all(),
        field_name='channel',
        label=_('Channel'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant',
        label=_('Tenant'),
    )

    class Meta:
        model = OpticalCircuit
        fields = ('id', 'name', 'status', 'channel', 'tenant')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class OpticalCircuitHopFilterSet(NetBoxModelFilterSet):
    optical_circuit_id = django_filters.ModelMultipleChoiceFilter(
        queryset=OpticalCircuit.objects.all(),
        field_name='optical_circuit',
        label=_('Optical circuit'),
    )
    interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name='interface',
        label=_('Interface'),
    )

    class Meta:
        model = OpticalCircuitHop
        fields = ('id', 'optical_circuit', 'sequence', 'interface', 'port_role')

    def search(self, queryset, name, value):
        return queryset.filter(optical_circuit__name__icontains=value)


class MultiplexGroupFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device',
        label=_('Device'),
    )

    class Meta:
        model = MultiplexGroup
        fields = ('id', 'name', 'device')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class MultiplexGroupMemberFilterSet(NetBoxModelFilterSet):
    group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=MultiplexGroup.objects.all(),
        field_name='group',
        label=_('Multiplex group'),
    )
    channel_id = django_filters.ModelMultipleChoiceFilter(
        queryset=WavelengthChannel.objects.all(),
        field_name='channel',
        label=_('Channel'),
    )

    class Meta:
        model = MultiplexGroupMember
        fields = ('id', 'group', 'client_interface', 'channel')

    def search(self, queryset, name, value):
        return queryset.filter(group__name__icontains=value)
