import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable

from .models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    MultiplexGroup,
)


class WavelengthGridTable(NetBoxTable):
    name = tables.Column(linkify=True)
    grid_type = tables.Column(verbose_name=_('Grid Type'))
    channel_count = tables.Column(
        verbose_name=_('Channels'),
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = WavelengthGrid
        fields = ('pk', 'id', 'name', 'grid_type', 'channel_count', 'description')
        default_columns = ('pk', 'name', 'grid_type', 'channel_count')


class WavelengthChannelTable(NetBoxTable):
    name = tables.Column(linkify=True)
    grid = tables.Column(linkify=True)
    frequency_ghz = tables.Column(verbose_name=_('Frequency (GHz)'))
    wavelength_nm = tables.Column(verbose_name=_('Wavelength (nm)'))
    width_ghz = tables.Column(verbose_name=_('Width (GHz)'))

    class Meta(NetBoxTable.Meta):
        model = WavelengthChannel
        fields = ('pk', 'id', 'name', 'grid', 'frequency_ghz', 'wavelength_nm', 'width_ghz')
        default_columns = ('pk', 'name', 'grid', 'frequency_ghz', 'wavelength_nm')


class OpticalCircuitTable(NetBoxTable):
    name = tables.Column(linkify=True)
    channel = tables.Column(linkify=True)
    status = tables.Column()
    tenant = tables.Column(linkify=True)
    hop_count = tables.Column(
        verbose_name=_('Hops'),
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = OpticalCircuit
        fields = ('pk', 'id', 'name', 'channel', 'status', 'tenant', 'hop_count', 'description')
        default_columns = ('pk', 'name', 'channel', 'status', 'tenant', 'hop_count')


class MultiplexGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    line_interface = tables.Column(linkify=True, verbose_name=_('Line Port'))
    member_count = tables.Column(
        verbose_name=_('Client Ports'),
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = MultiplexGroup
        fields = ('pk', 'id', 'name', 'device', 'line_interface', 'member_count', 'description')
        default_columns = ('pk', 'name', 'device', 'line_interface', 'member_count')
