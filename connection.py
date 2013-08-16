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
import socket
import threading

class Connection():
    def __init__(self, spec):
        self.spec = spec
        self.socket = socket.socket()
        self.spec._connect(self.socket)
        threading.Thread(target=self.recvloop, name="Thread-Recv-Loop").start()

    def recvloop(self):
        while True:
            text = self.socket.recv(1024).strip()
            logging.getLogger("pyrc.connection.recvloop").debug(text)
