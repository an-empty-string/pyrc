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
    def __init__(self, host, port=6667, password=""):
        self.host = host
        self.port = port
        self.password = password

    def _connect(self, sock):
        logging.getLogger("pyrc.serverspec")\
                .info("Connecting to %s:%s" % (self.host, self.port))
        sock.connect((self.host, self.port))
        if self.password != "":
            logging.getLogger("pyrc.serverspec")\
                    .debug("Sending server password")
            sock.send("PASS %s" % self.password)
