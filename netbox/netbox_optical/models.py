from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel, PrimaryModel


class WavelengthGrid(PrimaryModel):
    """
    A wavelength grid defines a set of channel slots. Grids may represent
    standard ITU-T allocations (e.g. DWDM C-band at 50 GHz or 100 GHz spacing,
    CWDM) or custom/proprietary allocations.
    """
    class GridTypeChoices(models.TextChoices):
        DWDM_100GHZ = 'dwdm-100ghz', _('DWDM 100 GHz')
        DWDM_50GHZ = 'dwdm-50ghz', _('DWDM 50 GHz')
        DWDM_75GHZ = 'dwdm-75ghz', _('DWDM 75 GHz')
        DWDM_FLEXGRID = 'dwdm-flexgrid', _('DWDM Flex Grid')
        CWDM = 'cwdm', _('CWDM')
        CUSTOM = 'custom', _('Custom')

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    grid_type = models.CharField(
        max_length=50,
        choices=GridTypeChoices.choices,
        verbose_name=_('Grid type'),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('wavelength grid')
        verbose_name_plural = _('wavelength grids')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:wavelengthgrid', args=[self.pk])


class WavelengthChannel(NetBoxModel):
    """
    A specific channel on a wavelength grid, identified by name/number,
    center frequency, and center wavelength.

    For fixed grids the channel width is implied by the grid spacing.
    For flex-grid, the width_ghz field records the allocated spectral width.
    """
    grid = models.ForeignKey(
        to=WavelengthGrid,
        on_delete=models.CASCADE,
        related_name='channels',
    )
    name = models.CharField(
        max_length=50,
        help_text=_('Channel identifier, e.g. C21, Ch 32, 1550'),
    )
    frequency_ghz = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Frequency (GHz)'),
        help_text=_('Center frequency in GHz'),
    )
    wavelength_nm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name=_('Wavelength (nm)'),
        help_text=_('Center wavelength in nm'),
    )
    width_ghz = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Width (GHz)'),
        help_text=_('Channel width in GHz (primarily for flex-grid)'),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['grid', 'frequency_ghz']
        unique_together = ['grid', 'name']
        verbose_name = _('wavelength channel')
        verbose_name_plural = _('wavelength channels')

    def __str__(self):
        return f'{self.grid.name}: {self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:wavelengthchannel', args=[self.pk])


class OpticalCircuit(PrimaryModel):
    """
    An end-to-end lightpath carrying a service on a specific wavelength channel.

    An optical circuit traverses one or more physical interfaces (recorded as
    OpticalCircuitHop instances) and can optionally be associated with a tenant
    to support service-to-wavelength correlation.
    """
    class StatusChoices(models.TextChoices):
        PLANNED = 'planned', _('Planned')
        PROVISIONING = 'provisioning', _('Provisioning')
        ACTIVE = 'active', _('Active')
        DECOMMISSIONING = 'decommissioning', _('Decommissioning')
        DECOMMISSIONED = 'decommissioned', _('Decommissioned')

    name = models.CharField(
        max_length=200,
        unique=True,
    )
    channel = models.ForeignKey(
        to=WavelengthChannel,
        on_delete=models.PROTECT,
        related_name='optical_circuits',
        help_text=_('Wavelength channel this circuit operates on'),
    )
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.SET_NULL,
        related_name='optical_circuits',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('optical circuit')
        verbose_name_plural = _('optical circuits')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:opticalcircuit', args=[self.pk])


class OpticalCircuitHop(NetBoxModel):
    """
    An ordered hop in an optical circuit's end-to-end path.

    Each hop references an interface on a device. The sequence field
    determines the order of traversal. The port_role field indicates
    whether the interface is acting as a client port, line port,
    add/drop port, or express (pass-through) port at this hop.
    """
    class PortRoleChoices(models.TextChoices):
        CLIENT = 'client', _('Client')
        LINE = 'line', _('Line')
        ADD = 'add', _('Add')
        DROP = 'drop', _('Drop')
        EXPRESS = 'express', _('Express (pass-through)')

    optical_circuit = models.ForeignKey(
        to=OpticalCircuit,
        on_delete=models.CASCADE,
        related_name='hops',
    )
    sequence = models.PositiveIntegerField(
        help_text=_('Order of this hop in the lightpath (lower = earlier)'),
    )
    interface = models.ForeignKey(
        to='dcim.Interface',
        on_delete=models.CASCADE,
        related_name='optical_circuit_hops',
    )
    port_role = models.CharField(
        max_length=50,
        choices=PortRoleChoices.choices,
        blank=True,
        verbose_name=_('Port role'),
    )

    class Meta:
        ordering = ['optical_circuit', 'sequence']
        unique_together = ['optical_circuit', 'sequence']
        verbose_name = _('optical circuit hop')
        verbose_name_plural = _('optical circuit hops')

    def __str__(self):
        return f'{self.optical_circuit.name} hop {self.sequence}: {self.interface}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:opticalcircuithop', args=[self.pk])


class MultiplexGroup(PrimaryModel):
    """
    Represents the internal optical relationship within a MUX/DEMUX,
    transponder, or similar device where multiple client-side ports
    map to a single line-side (network) port.

    The line_interface is the combined/aggregate output port.
    Client ports are added as MultiplexGroupMember instances.
    """
    name = models.CharField(
        max_length=200,
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='multiplex_groups',
    )
    line_interface = models.ForeignKey(
        to='dcim.Interface',
        on_delete=models.CASCADE,
        related_name='multiplex_line_groups',
        verbose_name=_('Line port'),
        help_text=_('The line-side (network) aggregate port'),
    )

    class Meta:
        ordering = ['device', 'name']
        unique_together = ['device', 'name']
        verbose_name = _('multiplex group')
        verbose_name_plural = _('multiplex groups')

    def __str__(self):
        return f'{self.device.name}: {self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:multiplexgroup', args=[self.pk])


class MultiplexGroupMember(NetBoxModel):
    """
    A client port within a multiplex group, optionally assigned to a
    specific wavelength channel.

    When a channel is assigned, it indicates which wavelength this
    client port's signal occupies on the line-side aggregate fiber.
    """
    group = models.ForeignKey(
        to=MultiplexGroup,
        on_delete=models.CASCADE,
        related_name='members',
    )
    client_interface = models.ForeignKey(
        to='dcim.Interface',
        on_delete=models.CASCADE,
        related_name='multiplex_memberships',
        verbose_name=_('Client port'),
    )
    channel = models.ForeignKey(
        to=WavelengthChannel,
        on_delete=models.SET_NULL,
        related_name='multiplex_assignments',
        blank=True,
        null=True,
        help_text=_('Wavelength channel assigned to this client port'),
    )

    class Meta:
        ordering = ['group', 'client_interface']
        unique_together = ['group', 'client_interface']
        verbose_name = _('multiplex group member')
        verbose_name_plural = _('multiplex group members')

    def __str__(self):
        channel_str = f' ({self.channel.name})' if self.channel else ''
        return f'{self.group.name}: {self.client_interface.name}{channel_str}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_optical:multiplexgroupmember', args=[self.pk])
