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


import data.numerics
import re


class Filter():
    def __init__(self):
        pass

    def run(self, text):
        return False


class DefaultFilter(Filter):
    def run(self, text):
        return False


class PingFilter(Filter):
    def run(self, text):
        if text.split()[0] == "PING":
            return True
        return False


class EndMOTDFilter(Filter):
    def run(self, text):
        if data.numerics.numerics["RPL_ENDOFMOTD"] in text or\
                data.numerics.numerics["ERR_NOMOTD"] in text:
            return True
        return False


class PrivmsgFilter(Filter):
    def run(self, text):
        if re.match(":(.*!.*@.*) PRIVMSG (.*) :(.*)", text):
            return True
        return False


class NickInUseFilter(Filter):
    def run(self, text):
        if data.numerics.numerics["ERR_NICKNAMEINUSE"] in text:
            return True
        return False


class EndWhoisFilter(Filter):
    def run(self, text):
        if data.numerics.numerics["RPL_ENDOFWHOIS"] in text:
            return True
        return False


class WhoisDataFilter(Filter):
    def run(self, text):
        numeric = text.split()[1]
        if numeric in ["311", "312", "313", "317", "319", "330"]:
            return True
        return False
