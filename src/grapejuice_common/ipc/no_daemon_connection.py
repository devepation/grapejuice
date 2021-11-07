import logging
from typing import Callable

from grapejuice_common.ipc.i_dbus_connection import IDBusConnection
from grapejuice_common.wine.wineprefix import Wineprefix

LOG = logging.getLogger(__name__)


def _with_prefix_id(prefix_id: str, cb: Callable[[Wineprefix], None]):
    from grapejuice_common.wine.wine_functions import find_wineprefix

    prefix = find_wineprefix(prefix_id)

    if prefix.roblox.is_installed:
        cb(prefix)

    else:
        prefix.roblox.install_roblox(post_install_function=lambda: cb(prefix))


class NoDaemonModeConnection(IDBusConnection):
    @property
    def connected(self):
        return True

    def launch_studio(self, prefix_id: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.run_roblox_studio())

    def play_game(self, prefix_id: str, uri: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.run_roblox_player(uri))

    def edit_local_game(self, prefix_id: str, place_path: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.run_roblox_studio(uri=place_path))

    def edit_cloud_game(self, prefix_id: str, uri: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.run_roblox_studio(uri))

    def version(self):
        from grapejuiced import __version__

        return __version__

    def extract_fast_flags(self, prefix_id: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.extract_fast_flags())

    def install_roblox(self, prefix_id: str):
        _with_prefix_id(prefix_id, lambda prefix: prefix.roblox.install_roblox())
