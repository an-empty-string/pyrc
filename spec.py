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


import logging


class ServerSpec():
    """
    ServerSpec represents the information needed to connect to a server.
    """
    def __init__(self, userspec, host="irc.freenode.org", port=6667,
                 password=""):
        """
        Initializes a ServerSpec. The only required argument is a UserSpec,
        however, a host, port, and password can be specified. If they are not,
        they default to irc.freenode.org, 6667, and a blank string,
        respectively.
        """
        self.host = host
        self.port = port
        self.password = password
        self.userspec = userspec

    def _connect(self, connection):
        logging.getLogger("pyrc.serverspec") \
            .info("Connecting to %s:%s" % (self.host, self.port))
        connection._socket.connect((self.host, self.port))
        if self.password != "":
            logging.getLogger("pyrc.serverspec") \
                .debug("Sending server password")
            connection.send_raw("PASS %s\n" % self.password)
        self.userspec._send_info(connection)


class UserSpec():
    """
    UserSpec represents the information needed to identify to an IRC server.
    """
    def __init__(self, nick, ident=None, realname=None):
        """
        Initializes a UserSpec. The only required argument is a nickname,
        however, an ident and realname can be specified. If they are not,
        they default to the nickname.
        """
        self.nick = nick
        self.ident = nick if ident is None else ident
        self.realname = nick if realname is None else realname

    def _send_info(self, connection):
        logging.getLogger("pyrc.userspec").info("Sending nick/user")
        connection.send_raw("USER %s 0 * :%s\n" % (self.ident, self.realname))
        connection.nickname_negotiation = True
        connection.send_raw("NICK %s\n" % self.nick)
