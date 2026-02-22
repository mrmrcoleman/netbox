from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox.ui import layout
from netbox.ui.panels import CommentsPanel, ObjectAttributesPanel, ObjectsTablePanel
from netbox.ui import attrs
from netbox.views import generic
from utilities.views import register_model_view

from .models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)
from .tables import (
    WavelengthGridTable,
    WavelengthChannelTable,
    OpticalCircuitTable,
    MultiplexGroupTable,
)
from .forms import (
    WavelengthGridForm,
    WavelengthChannelForm,
    OpticalCircuitForm,
    OpticalCircuitHopForm,
    MultiplexGroupForm,
    MultiplexGroupMemberForm,
)
from .filtersets import (
    WavelengthGridFilterSet,
    WavelengthChannelFilterSet,
    OpticalCircuitFilterSet,
    MultiplexGroupFilterSet,
)


#
# WavelengthGrid
#

class WavelengthGridPanel(ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    grid_type = attrs.ChoiceAttr('grid_type', label=_('Grid Type'))
    description = attrs.TextAttr('description', label=_('Description'))


@register_model_view(WavelengthGrid, 'list', path='', detail=False)
class WavelengthGridListView(generic.ObjectListView):
    queryset = WavelengthGrid.objects.annotate(channel_count=Count('channels'))
    table = WavelengthGridTable
    filterset = WavelengthGridFilterSet


@register_model_view(WavelengthGrid)
class WavelengthGridView(generic.ObjectView):
    queryset = WavelengthGrid.objects.all()
    layout = layout.SimpleLayout(
        left_panels=[
            WavelengthGridPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            CommentsPanel(),
        ],
        bottom_panels=[
            ObjectsTablePanel(
                model='netbox_optical.wavelengthchannel',
                filters=lambda ctx: {'grid_id': ctx['object'].pk},
                title=_('Channels'),
            ),
        ],
    )


@register_model_view(WavelengthGrid, 'add', detail=False)
@register_model_view(WavelengthGrid, 'edit')
class WavelengthGridEditView(generic.ObjectEditView):
    queryset = WavelengthGrid.objects.all()
    form = WavelengthGridForm


@register_model_view(WavelengthGrid, 'delete')
class WavelengthGridDeleteView(generic.ObjectDeleteView):
    queryset = WavelengthGrid.objects.all()


#
# WavelengthChannel
#

class WavelengthChannelPanel(ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    grid = attrs.RelatedObjectAttr('grid', label=_('Grid'), linkify=True)
    frequency_ghz = attrs.NumericAttr('frequency_ghz', label=_('Frequency (GHz)'))
    wavelength_nm = attrs.NumericAttr('wavelength_nm', label=_('Wavelength (nm)'))
    width_ghz = attrs.NumericAttr('width_ghz', label=_('Width (GHz)'))


@register_model_view(WavelengthChannel, 'list', path='', detail=False)
class WavelengthChannelListView(generic.ObjectListView):
    queryset = WavelengthChannel.objects.all()
    table = WavelengthChannelTable
    filterset = WavelengthChannelFilterSet


@register_model_view(WavelengthChannel)
class WavelengthChannelView(generic.ObjectView):
    queryset = WavelengthChannel.objects.all()
    layout = layout.SimpleLayout(
        left_panels=[
            WavelengthChannelPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
        ],
    )


@register_model_view(WavelengthChannel, 'add', detail=False)
@register_model_view(WavelengthChannel, 'edit')
class WavelengthChannelEditView(generic.ObjectEditView):
    queryset = WavelengthChannel.objects.all()
    form = WavelengthChannelForm


@register_model_view(WavelengthChannel, 'delete')
class WavelengthChannelDeleteView(generic.ObjectDeleteView):
    queryset = WavelengthChannel.objects.all()


#
# OpticalCircuit
#

class OpticalCircuitPanel(ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    channel = attrs.RelatedObjectAttr('channel', label=_('Channel'), linkify=True)
    status = attrs.ChoiceAttr('status', label=_('Status'))
    tenant = attrs.RelatedObjectAttr('tenant', label=_('Tenant'), linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))


@register_model_view(OpticalCircuit, 'list', path='', detail=False)
class OpticalCircuitListView(generic.ObjectListView):
    queryset = OpticalCircuit.objects.annotate(hop_count=Count('hops'))
    table = OpticalCircuitTable
    filterset = OpticalCircuitFilterSet


@register_model_view(OpticalCircuit)
class OpticalCircuitView(generic.ObjectView):
    queryset = OpticalCircuit.objects.all()
    layout = layout.SimpleLayout(
        left_panels=[
            OpticalCircuitPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            CommentsPanel(),
        ],
        bottom_panels=[
            ObjectsTablePanel(
                model='netbox_optical.opticalcircuithop',
                filters=lambda ctx: {'optical_circuit_id': ctx['object'].pk},
                title=_('Lightpath Hops'),
            ),
        ],
    )


@register_model_view(OpticalCircuit, 'add', detail=False)
@register_model_view(OpticalCircuit, 'edit')
class OpticalCircuitEditView(generic.ObjectEditView):
    queryset = OpticalCircuit.objects.all()
    form = OpticalCircuitForm


@register_model_view(OpticalCircuit, 'delete')
class OpticalCircuitDeleteView(generic.ObjectDeleteView):
    queryset = OpticalCircuit.objects.all()


#
# OpticalCircuitHop
#

@register_model_view(OpticalCircuitHop, 'add', detail=False)
@register_model_view(OpticalCircuitHop, 'edit')
class OpticalCircuitHopEditView(generic.ObjectEditView):
    queryset = OpticalCircuitHop.objects.all()
    form = OpticalCircuitHopForm


@register_model_view(OpticalCircuitHop, 'delete')
class OpticalCircuitHopDeleteView(generic.ObjectDeleteView):
    queryset = OpticalCircuitHop.objects.all()


#
# MultiplexGroup
#

class MultiplexGroupPanel(ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    device = attrs.RelatedObjectAttr('device', label=_('Device'), linkify=True)
    line_interface = attrs.RelatedObjectAttr('line_interface', label=_('Line Port'), linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))


@register_model_view(MultiplexGroup, 'list', path='', detail=False)
class MultiplexGroupListView(generic.ObjectListView):
    queryset = MultiplexGroup.objects.annotate(member_count=Count('members'))
    table = MultiplexGroupTable
    filterset = MultiplexGroupFilterSet


@register_model_view(MultiplexGroup)
class MultiplexGroupView(generic.ObjectView):
    queryset = MultiplexGroup.objects.all()
    layout = layout.SimpleLayout(
        left_panels=[
            MultiplexGroupPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            CommentsPanel(),
        ],
        bottom_panels=[
            ObjectsTablePanel(
                model='netbox_optical.multiplexgroupmember',
                filters=lambda ctx: {'group_id': ctx['object'].pk},
                title=_('Client Ports'),
            ),
        ],
    )


@register_model_view(MultiplexGroup, 'add', detail=False)
@register_model_view(MultiplexGroup, 'edit')
class MultiplexGroupEditView(generic.ObjectEditView):
    queryset = MultiplexGroup.objects.all()
    form = MultiplexGroupForm


@register_model_view(MultiplexGroup, 'delete')
class MultiplexGroupDeleteView(generic.ObjectDeleteView):
    queryset = MultiplexGroup.objects.all()


#
# MultiplexGroupMember
#

@register_model_view(MultiplexGroupMember, 'add', detail=False)
@register_model_view(MultiplexGroupMember, 'edit')
class MultiplexGroupMemberEditView(generic.ObjectEditView):
    queryset = MultiplexGroupMember.objects.all()
    form = MultiplexGroupMemberForm


@register_model_view(MultiplexGroupMember, 'delete')
class MultiplexGroupMemberDeleteView(generic.ObjectDeleteView):
    queryset = MultiplexGroupMember.objects.all()
