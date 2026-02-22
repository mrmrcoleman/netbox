from rest_framework import serializers

from dcim.api.serializers import InterfaceSerializer, DeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer

from ..models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)


class WavelengthGridSerializer(NetBoxModelSerializer):
    channel_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = WavelengthGrid
        fields = (
            'id', 'url', 'display', 'name', 'grid_type', 'description',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
            'channel_count',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'grid_type')


class WavelengthChannelSerializer(NetBoxModelSerializer):
    grid = WavelengthGridSerializer(nested=True)

    class Meta:
        model = WavelengthChannel
        fields = (
            'id', 'url', 'display', 'grid', 'name', 'frequency_ghz',
            'wavelength_nm', 'width_ghz', 'tags', 'custom_fields',
            'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'frequency_ghz', 'wavelength_nm')


class OpticalCircuitSerializer(NetBoxModelSerializer):
    channel = WavelengthChannelSerializer(nested=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    hop_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = OpticalCircuit
        fields = (
            'id', 'url', 'display', 'name', 'channel', 'status', 'tenant',
            'description', 'comments', 'tags', 'custom_fields',
            'created', 'last_updated', 'hop_count',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'status')


class OpticalCircuitHopSerializer(NetBoxModelSerializer):
    optical_circuit = OpticalCircuitSerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = OpticalCircuitHop
        fields = (
            'id', 'url', 'display', 'optical_circuit', 'sequence',
            'interface', 'port_role', 'tags', 'custom_fields',
            'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'sequence', 'port_role')


class MultiplexGroupSerializer(NetBoxModelSerializer):
    device = DeviceSerializer(nested=True)
    line_interface = InterfaceSerializer(nested=True)
    member_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = MultiplexGroup
        fields = (
            'id', 'url', 'display', 'name', 'device', 'line_interface',
            'description', 'comments', 'tags', 'custom_fields',
            'created', 'last_updated', 'member_count',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class MultiplexGroupMemberSerializer(NetBoxModelSerializer):
    group = MultiplexGroupSerializer(nested=True)
    client_interface = InterfaceSerializer(nested=True)
    channel = WavelengthChannelSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = MultiplexGroupMember
        fields = (
            'id', 'url', 'display', 'group', 'client_interface', 'channel',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display')
