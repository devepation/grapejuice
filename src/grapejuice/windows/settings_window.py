import logging
from typing import Optional

from gi.repository import Gtk

from grapejuice import gui_task_manager
from grapejuice.tasks import PerformUpdate
from grapejuice_common import paths, uninstall
from grapejuice_common.gtk.components.grape_setting import GrapeSetting
from grapejuice_common.gtk.components.grape_setting_action import GrapeSettingAction
from grapejuice_common.gtk.components.grape_settings_group import GrapeSettingsGroup
from grapejuice_common.gtk.components.grape_settings_pane import GrapeSettingsPane
from grapejuice_common.gtk.gtk_base import GtkBase, handler
from grapejuice_common.gtk.gtk_util import dialog
from grapejuice_common.gtk.yes_no_dialog import yes_no_dialog
from grapejuice_common.uninstall import UninstallationParameters
from grapejuice_common.update_info_providers import UpdateInformationProvider
from grapejuice_common.util import xdg_open


def _from_user_settings(key: str, default_value, **kwargs):
    from grapejuice_common.features.settings import current_settings

    return GrapeSetting(
        key=key,
        value=current_settings.get(key, default_value),
        **kwargs
    )


def _do_reinstall_grapejuice():
    from grapejuice_common import update_info_providers

    provider: UpdateInformationProvider = update_info_providers.guess_relevant_provider()
    if not provider.can_update():
        return

    gui_task_manager.run_task_once(PerformUpdate, provider, reopen=True)


def _do_uninstall_grapejuice():
    log = logging.getLogger("settings/uninstall")

    do_it = yes_no_dialog("Uninstall Grapejuice", "Are you sure that you want to uninstall Grapejuice?")
    if not do_it:
        return

    parameters = UninstallationParameters(
        remove_prefix=yes_no_dialog(
            title="Remove Wineprefixes?",
            message="Do you want to remove all the Wineprefixes Grapejuice has created? Doing this will permanently "
                    "remove all Roblox program files from this machine. If you have stored Roblox experiences or "
                    "models inside of a Wineprefix, these will be deleted as well. "
        ),
        for_reals=True
    )

    try:
        dialog("Grapejuice will now uninstall itself, the program will close when the process is finished.")
        uninstall.go(parameters)

    except Exception as e:
        msg = f"{e.__class__.__name__}: {str(e)}"
        log.error(msg)

        dialog(f"Failed to uninstall Grapejuice.\n\n{msg}")


def _install_actions():
    from grapejuice_common import update_info_providers

    provider: UpdateInformationProvider = update_info_providers.guess_relevant_provider()
    if not provider.can_update():
        return None

    return GrapeSettingsGroup(
        title="Installation Actions",
        description="Manage your Grapejuice installation",
        settings=[
            GrapeSetting(
                key="re-install",
                display_name="Re-install",
                description="Performing this action will re-install Grapejuice.",
                value=GrapeSettingAction(
                    key="re-install",
                    display_name="Re-install",
                    action=lambda *_: _do_reinstall_grapejuice()
                ),
            ),
            GrapeSetting(
                key="uninstall",
                display_name="Uninstall",
                description="Completely remove Grapejuice from your system!",
                value=GrapeSettingAction(
                    key="uninstall",
                    display_name="Uninstall",
                    action=lambda *_: _do_uninstall_grapejuice()
                ),
            )
        ]
    )


def _general_settings():
    return GrapeSettingsGroup(
        title="General",
        description="These are general Grapejuice settings",
        settings=[
            _from_user_settings(
                key="show_fast_flag_warning",
                default_value=True,
                display_name="Show Fast Flag Warning",
                description="Should Grapejuice warn you when opening the Fast Flag Editor?"
            ),
            _from_user_settings(
                key="no_daemon_mode",
                default_value=True,
                display_name="Use Grapejuice daemon",
                description="Enable or Disable the Grapejuice Daemon. This is an advanced debugging feature only "
                            "meant for people who work on Wine itself.",
                bidirectional_transformer=lambda b: not b
            ),
            _from_user_settings(
                key="disable_updates",
                default_value=False,
                display_name="Disable self-updater"
            ),
            _from_user_settings(
                key="ignore_wine_version",
                default_value=False,
                display_name="Ignore Wine version"
            ),
            _from_user_settings(
                key="release_channel",
                default_value="master",
                display_name="Release Channel",
                description="Determines from which branch Grapejuice should be updated. This only works for source "
                            "installs. "
            )
        ]
    )


class SettingsWindow(GtkBase):
    _settings_pane: GrapeSettingsPane
    _general_settings: GrapeSettingsGroup
    _initial_general_settings: str

    def __init__(self):
        super().__init__(
            glade_path=paths.settings_glade(),
            handler_instance=self,
            root_widget_name="grapejuice_settings"
        )

        self._general_settings = _general_settings()
        self._initial_general_settings = self._general_settings.settings_json

        self._settings_pane = GrapeSettingsPane(
            groups=list(filter(None, [self._general_settings, _install_actions()]))
        )
        self._settings_pane.show()

        self.widgets.settings_pane_parent.add(self._settings_pane)

    @handler
    def open_settings_file(self, *_):
        xdg_open(paths.grapejuice_user_settings())

    def _save_general_settings(self, should_save_override: Optional[bool] = False):
        should_save = should_save_override or self._initial_general_settings != self._general_settings.settings_json

        if should_save:
            from grapejuice_common.features.settings import current_settings

            for k, v in self._general_settings.settings_dictionary.items():
                current_settings.set(k, v)

            current_settings.save()

    @handler
    def on_destroy(self, _):
        self._save_general_settings()

    def show(self):
        self.root_widget.set_position(Gtk.WindowPosition.CENTER)
        self.root_widget.show_all()