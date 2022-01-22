/*
 * View model for Active Connections
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function ActiveconnectionsViewModel(parameters) {
        var self = this;

        self.active_connections = ko.observableArray([]);

        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== "activeconnections") {
                return;
            }

            self.active_connections(data["active_connections"]);
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: ActiveconnectionsViewModel,
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        elements: [ "#sidebar_plugin_activeconnections" ]
    });
});
