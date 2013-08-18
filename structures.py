#     //   ) )          //   ) )  //   ) )
#    //___/ /          //___/ /  //
#   / ____ / //   / / / ___ (   //
#  //       ((___/ / //   | |  //
# //            / / //    | | ((____/ /
#
# This file is part of PyRC.
#
#    PyRC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyRC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyRC.  If not, see <http://www.gnu.org/licenses/>.
#


import filters
import logging


class User():
    """
    User represents an IRC user.
    """
    def __init__(self, hostmask):
        """
        Initialize a User given a hostmask.
        """
        self.nick = hostmask.split("!")[0]
        self.userhost = hostmask.split("!")[1]
        self.user = self.userhost.split("@")[0]
        self.host = self.userhost.split("@")[1]
        self.waiting_for_server = False

    def whois(self, connection):
        self.waiting_for_server = True
        self._conn = connection
        self._whois_data = []
        connection.send_raw("WHOIS %s\n" % self.nick)
        connection.dispatcher.attach_destination(self._end_whois,
                                                 filters.EndWhoisFilter)
        connection.dispatcher.attach_destination(self._proc_whois,
                                                 filters.WhoisDataFilter)
        while self.waiting_for_server:
            pass
        print self._whois_data

    def _proc_whois(self, text):
        logging.getLogger("pyrc.user.whois").debug(text)
        self._whois_data.append(text)

    def _end_whois(self, text):
        logging.getLogger("pyrc.user.whois").debug("End of WHOIS.")
        self.waiting_for_server = False
        self._conn.dispatcher.detach_destination(self._end_whois)
        self._conn.dispatcher.detach_destination(self._proc_whois)
        del self._conn


class Channel():
    """
    Channel represents an IRC channel.
    """
    def __init__(self, chan):
        """
        Initialize a channel.
        """
        self.chan = chan


class IncomingMessageDispatcher():
    """
    IncomingMessageDispatcher is an internally used class to keep track of
    incoming messages.
    """
    def __init__(self):
        self._destinations = {}

    def dispatch(self, message):
        for (mdest, mfilter) in self._destinations.items():
            if mfilter().run(message):
                mdest(message)

    def attach_destination(self, dest, dfilter=filters.DefaultFilter):
        self._destinations[dest] = dfilter

    def detach_destination(self, dest):
        try:
            del self._destinations[dest]
        except:
            pass
