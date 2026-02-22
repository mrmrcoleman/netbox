from django.urls import include, path

from utilities.urls import get_model_urls

from .models import (
    WavelengthGrid,
    WavelengthChannel,
    OpticalCircuit,
    OpticalCircuitHop,
    MultiplexGroup,
    MultiplexGroupMember,
)

urlpatterns = (
    # Wavelength grids
    path('grids/', include(get_model_urls('netbox_optical', 'wavelengthgrid', detail=False))),
    path('grids/<int:pk>/', include(get_model_urls('netbox_optical', 'wavelengthgrid'))),

    # Wavelength channels
    path('channels/', include(get_model_urls('netbox_optical', 'wavelengthchannel', detail=False))),
    path('channels/<int:pk>/', include(get_model_urls('netbox_optical', 'wavelengthchannel'))),

    # Optical circuits
    path('circuits/', include(get_model_urls('netbox_optical', 'opticalcircuit', detail=False))),
    path('circuits/<int:pk>/', include(get_model_urls('netbox_optical', 'opticalcircuit'))),

    # Optical circuit hops
    path('hops/', include(get_model_urls('netbox_optical', 'opticalcircuithop', detail=False))),
    path('hops/<int:pk>/', include(get_model_urls('netbox_optical', 'opticalcircuithop'))),

    # Multiplex groups
    path('multiplex-groups/', include(get_model_urls('netbox_optical', 'multiplexgroup', detail=False))),
    path('multiplex-groups/<int:pk>/', include(get_model_urls('netbox_optical', 'multiplexgroup'))),

    # Multiplex group members
    path('multiplex-members/', include(get_model_urls('netbox_optical', 'multiplexgroupmember', detail=False))),
    path('multiplex-members/<int:pk>/', include(get_model_urls('netbox_optical', 'multiplexgroupmember'))),
)
