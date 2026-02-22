from rest_framework import routers

from .views import (
    WavelengthGridViewSet,
    WavelengthChannelViewSet,
    OpticalCircuitViewSet,
    OpticalCircuitHopViewSet,
    MultiplexGroupViewSet,
    MultiplexGroupMemberViewSet,
)

router = routers.DefaultRouter()
router.register('wavelength-grids', WavelengthGridViewSet)
router.register('wavelength-channels', WavelengthChannelViewSet)
router.register('optical-circuits', OpticalCircuitViewSet)
router.register('optical-circuit-hops', OpticalCircuitHopViewSet)
router.register('multiplex-groups', MultiplexGroupViewSet)
router.register('multiplex-group-members', MultiplexGroupMemberViewSet)

urlpatterns = router.urls
