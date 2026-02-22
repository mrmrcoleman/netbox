from django.utils.translation import gettext_lazy as _

from dcim.models import Device, Interface
from netbox.forms import NetBoxModelForm
from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField

from .models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)


class WavelengthGridForm(NetBoxModelForm):
    class Meta:
        model = WavelengthGrid
        fields = ('name', 'grid_type', 'description', 'comments', 'tags')


class WavelengthChannelForm(NetBoxModelForm):
    grid = DynamicModelChoiceField(
        queryset=WavelengthGrid.objects.all(),
    )

    class Meta:
        model = WavelengthChannel
        fields = ('grid', 'name', 'frequency_ghz', 'wavelength_nm', 'width_ghz', 'tags')


class OpticalCircuitForm(NetBoxModelForm):
    channel = DynamicModelChoiceField(
        queryset=WavelengthChannel.objects.all(),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
    )

    class Meta:
        model = OpticalCircuit
        fields = ('name', 'channel', 'status', 'tenant', 'description', 'comments', 'tags')


class OpticalCircuitHopForm(NetBoxModelForm):
    optical_circuit = DynamicModelChoiceField(
        queryset=OpticalCircuit.objects.all(),
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
    )

    class Meta:
        model = OpticalCircuitHop
        fields = ('optical_circuit', 'sequence', 'interface', 'port_role', 'tags')


class MultiplexGroupForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
    )
    line_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label=_('Line port'),
    )

    class Meta:
        model = MultiplexGroup
        fields = ('name', 'device', 'line_interface', 'description', 'comments', 'tags')


class MultiplexGroupMemberForm(NetBoxModelForm):
    group = DynamicModelChoiceField(
        queryset=MultiplexGroup.objects.all(),
    )
    client_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label=_('Client port'),
    )
    channel = DynamicModelChoiceField(
        queryset=WavelengthChannel.objects.all(),
        required=False,
    )

    class Meta:
        model = MultiplexGroupMember
        fields = ('group', 'client_interface', 'channel', 'tags')
