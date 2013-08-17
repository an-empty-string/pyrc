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
import logging
import socket
import threading

class Connection():
    def __init__(self, spec):
        self.spec = spec
        self.waiting_for_server = True
        self._handlers = []
        self._socket = socket.socket()
        self.spec._connect(self._socket)
        threading.Thread(target=self.recvloop, name="Thread-Recv-Loop").start()
        while self.waiting_for_server:
            pass

    def recvloop(self):
        while True:
            text = self._socket.recv(1024).strip()
            self._check_ping(text)
            if self.waiting_for_server:
                self._check_endmotd(text)
            logging.getLogger("pyrc.connection.recvloop").debug(text)

    def _check_ping(self, text):
        spltext = text.split()
        if spltext[0] == "PING":
            logging.getLogger("pyrc.connection.recvloop.checkping")\
                    .debug("Sending PONG")
            self.send_raw("PONG %s" % spltext[1])

    def _check_endmotd(self, text):
        if data.numerics.numerics["RPL_ENDOFMOTD"] in text:
            logging.getLogger("pyrc.connection.recvloop.checkmotd")\
                    .debug("End of MOTD.")
            self.waiting_for_server = False

    def send_raw(self, text):
        self._socket.send(text + "\n")

    def attach_handler(self, handler):
        self._handlers.append(handler)
