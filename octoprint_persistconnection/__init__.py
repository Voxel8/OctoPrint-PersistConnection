# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util import RepeatedTimer
from time import sleep

__author__ = "Kevin Murphy <kevin@voxel8.co>"
__license__ = ("GNU Affero General Public License "
               "http://www.gnu.org/licenses/agpl.html")
__copyright__ = ("Copyright (C) 2016 Voxel8, Inc. - "
                 "Released under terms of the AGPLv3 License")


class PersistConnectionPlugin(octoprint.plugin.StartupPlugin):

    def __init__(self):
        self._timer = None

    def on_after_startup(self):
        self._timer = RepeatedTimer(
            1.0, self._check_connection, run_first=True)
        self._timer.start()

    def _check_connection(self):
        state = self._printer.get_state_string()
        if state in ["Closed", "Offline"]:
            self._logger.info("Offline or closed; reconnecting")
            self._printer.connect()
        elif state == "Error":
            self._logger.info("Error detected; reconnecting in 30 seconds")
            sleep(30)
            self._printer.connect()

__plugin_name__ = "Persist Connection Plugin"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PersistConnectionPlugin()
