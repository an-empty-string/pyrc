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


import connection
import logging
import spec
import structures

if __name__ == "__main__":
    uspec = spec.UserSpec("pyrcbot", "fwilson", "fwilix bot")
    sspec = spec.ServerSpec(uspec, host="irc.freenode.org")

    logging.basicConfig(level=logging.DEBUG)

    conn = connection.Connection(sspec)
    conn.join("#pyrc-devel")
    structures.User("fwilson!bouncer@wikipedia/Fox-Wilson").whois(conn)
