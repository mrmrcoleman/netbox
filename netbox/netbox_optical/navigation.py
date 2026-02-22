from django.utils.translation import gettext_lazy as _

from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem

grids_item = PluginMenuItem(
    link='plugins:netbox_optical:wavelengthgrid_list',
    link_text=_('Wavelength Grids'),
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_optical:wavelengthgrid_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
        ),
    ),
)

channels_item = PluginMenuItem(
    link='plugins:netbox_optical:wavelengthchannel_list',
    link_text=_('Channels'),
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_optical:wavelengthchannel_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
        ),
    ),
)

circuits_item = PluginMenuItem(
    link='plugins:netbox_optical:opticalcircuit_list',
    link_text=_('Optical Circuits'),
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_optical:opticalcircuit_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
        ),
    ),
)

multiplex_item = PluginMenuItem(
    link='plugins:netbox_optical:multiplexgroup_list',
    link_text=_('Multiplex Groups'),
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_optical:multiplexgroup_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
        ),
    ),
)

menu = PluginMenu(
    label=_('Optical'),
    groups=(
        (_('Wavelengths'), (grids_item, channels_item)),
        (_('Circuits'), (circuits_item,)),
        (_('Multiplexing'), (multiplex_item,)),
    ),
    icon_class='mdi mdi-lightbulb-on-outline',
)

menu_items = (grids_item, channels_item, circuits_item, multiplex_item)
