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
import filters
import logging
import random
import re
import socket
import structures
import threading


class Connection():

    """
    A Connection represents a connection to an IRC server.
    """

    def __init__(self, spec):
        """
        Initialize a connection. Takes a ServerSpec as an argument.
        """
        self.spec = spec
        self.waiting_for_server = True
        self._handlers = []
        # Dispatcher
        self.dispatcher = structures.IncomingMessageDispatcher()
        self.dispatcher.attach_destination(self._handle_ping, 
                filters.PingFilter)
        self.dispatcher.attach_destination(self._handle_endmotd, 
                filters.EndMOTDFilter)
        self.dispatcher.attach_destination(self._handle_nickinuse, 
                filters.NickInUseFilter)
        self.dispatcher.attach_destination(self._handle_privmsg,
                filters.PrivmsgFilter)
        # End dispatcher
        self._socket = socket.socket()
        self.spec._connect(self)
        threading.Thread(target=self.recvloop, name="Thread-Recv-Loop").start()
        while self.waiting_for_server:
            pass

    def recvloop(self):
        """
        This function is automatically called by initializing the Connection.
        This handles all incoming messages from the server.
        """
        while True:
            text = self._socket.recv(1024).strip()
            logging.getLogger("pyrc.connection.recvloop").debug(text)
            self.dispatcher.dispatch(text)

    def send_raw(self, text):
        """
        Send a raw string to the IRC server.
        """
        self._socket.send(text + "\n")

    def attach_handler(self, handler):
        """
        Attach a subclass of Handler to the Connection. Events from the
        Connection will be passed to the relevant function in the handler.
        """
        self._handlers.append(handler)

    def join(self, chan):
        """
        Join a channel.
        """
        self.send_raw("JOIN %s" % chan)

    def part(self, chan):
        """
        Part a channel.
        """
        self.send_raw("PART %s" % chan)

    # Internally used methods    
    def _handle_ping(self, text):
        logging.getLogger("pyrc.connection.recvloop.checkping")\
                .debug("Sending PONG")
        self.send_raw("PONG %s" % text.split()[1])

    def _handle_endmotd(self, text):
        logging.getLogger("pyrc.connection.recvloop.checkmotd")\
                .debug("End of MOTD.")
        self.waiting_for_server = False
        self.dispatcher.detach_destination(self._handle_nickinuse)
        self.dispatcher.detach_destination(self._handle_endmotd)

    def _handle_nickinuse(self, text):
        self.spec.userspec.nick = self.spec.userspec.nick + "_"
        self.spec.userspec._send_info(self)

    def _handle_privmsg(self, text):
        match = re.match(":(.*!.*@.*) PRIVMSG (.*) :(.*)", text)
        hostmask = match.group(1)
        dest = match.group(2)
        message = match.group(3)
        logging.getLogger("pyrc.connection.recvloop.checkprivmsg")\
                .debug("PRIVMSG received, sent by %s to %s message %s" % (
                    hostmask, dest, message))

