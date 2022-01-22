# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events


class ActiveconnectionsPlugin(octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.EventHandlerPlugin,
                              ):

    def __init__(self):
        self.active_connections = []

    # ~~ EventHandlerPlugin mixin

    def on_event(self, event, payload):
        if event not in [Events.CLIENT_OPENED, Events.CLIENT_CLOSED]:
            return

        if event == Events.CLIENT_OPENED and payload["remoteAddress"] not in self.active_connections:
            self.active_connections.append(payload["remoteAddress"])

        if event == Events.CLIENT_CLOSED and payload["remoteAddress"] in self.active_connections:
            self.active_connections.remove(payload["remoteAddress"])

        self._logger.info(self.active_connections)
        self._plugin_manager.send_plugin_message(self._identifier, {"active_connections": self.active_connections})

    # ~~ TemplatePlugin mixin

    def get_template_configs(self):
        return [{'type': "sidebar", 'icon': "network-wired", 'custom_bindings': True,
                 'template': "activeconnections_sidebar.jinja2"}]

    # ~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "js": ["js/activeconnections.js"]
        }

    # ~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "activeconnections": {
                "displayName": "Active Connections",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-ActiveConnections",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jneilliii/OctoPrint-ActiveConnections/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Active Connections"
__plugin_pythoncompat__ = ">=3,<4"  # only python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ActiveconnectionsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
