from .echo import router as echo_router
from .help import router as help_router
from .start import router as start_router


def get_routers():
    return (start_router, help_router, echo_router)
