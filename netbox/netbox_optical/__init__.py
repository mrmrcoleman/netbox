from netbox.plugins import PluginConfig


class NetBoxOpticalConfig(PluginConfig):
    name = 'netbox_optical'
    verbose_name = 'NetBox Optical'
    version = '0.1.0'
    description = 'WDM (DWDM/CWDM) and optical-layer modeling for NetBox'
    base_url = 'optical'
    min_version = '4.5.0'
    max_version = '4.6.0'
    default_settings = {}


config = NetBoxOpticalConfig
