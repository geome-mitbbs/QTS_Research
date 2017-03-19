"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
Just a thin wrapper around a socket.
It allows us to keep some other info along with it.
"""


import socket
import threading
import logging

from ibapi.common import *
from ibapi.errors import *


#TODO: support SSL !!


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.wrapper = None
        self.lock = threading.Lock() 


    def connect(self):
        try:
            self.socket = socket.socket()
        #TODO: list the exceptions you want to catch
        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, FAIL_CREATE_SOCK.code(), FAIL_CREATE_SOCK.msg())

        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())
 
        self.socket.settimeout(1)   #non-blocking


    def disconnect(self):
        self.lock.acquire()
        try:
            logging.debug("disconnecting")
            self.socket.close()
            self.socket = None
            logging.debug("disconnected")
            if self.wrapper:
                self.wrapper.connectionClosed()
        finally:
            self.lock.release()


    def isConnected(self):
        #TODO: also handle when socket gets interrupted/error
        return self.socket is not None


    def sendMsg(self, msg):

        logging.debug("acquiring lock")
        self.lock.acquire()
        logging.debug("acquired lock")
        try:
            nSent = self.socket.send(msg)
        except socket.error:
            logging.debug("exception from sendMsg %s", sys.exc_info())
            raise
        finally:
            logging.debug("releasing lock")
            self.lock.release()
            logging.debug("release lock")
            
        logging.debug("sendMsg: sent: %d", nSent)

        return nSent


    def recvMsg(self):
        logging.debug("acquiring lock")
        self.lock.acquire()
        logging.debug("acquired lock")
        try:
            buf = self._recvAllMsg()
        except socket.error:
            logging.debug("exception from recvMsg %s", sys.exc_info())
            buf = b""
        else:
            pass
        finally:
            logging.debug("releasing lock")
            self.lock.release()
            logging.debug("release lock")

        return buf            
    

    def _recvAllMsg(self):
        cont = True
        allbuf = b""

        while cont:
            buf = self.socket.recv(4096)
            allbuf += buf
            logging.debug("len %d raw:%s|", len(buf), buf)

            if len(buf) < 4096:
                cont = False

        return allbuf  
             
