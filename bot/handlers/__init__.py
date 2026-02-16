from .admin import router as admin_router
from .echo import router as echo_router
from .help import router as help_router
from .language import router as language_router
from .settings import router as settings_router
from .start import router as start_router


def get_routers():
    return (
        start_router,
        settings_router,
        help_router,
        language_router,
        admin_router,
        echo_router,
    )
