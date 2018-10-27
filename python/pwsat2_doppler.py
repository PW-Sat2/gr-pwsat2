
from gnuradio import gr
import threading
import time
import socket
import numpy

class pwsat2_doppler(gr.sync_block):
    def __init__(self, callback, gpredict_host, gpredict_port, verbose):
        gr.sync_block.__init__(self,
                                name="PW-Sat2 Gpredict Doppler",
                                in_sig=None,
                                out_sig=[numpy.float32])

        self.callback = callback
        self.gpredict_host = gpredict_host
        self.gpredict_port = gpredict_port
        self.verbose = verbose

        self.isRunning = False
        self.server = None
        self.cur_freq  = 0

        print('Init Done')

    def work(self, input_items, output_items):
        output_items[0].fill(self.cur_freq)
        return len(output_items[0])

    def __gr_block_handle(self):        
        print(self.__message.action)
        gr.sync_block.__gr_block_handle(self)
        
    def start(self):
        print('start')
        bind_to = (self.gpredict_host, self.gpredict_port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(bind_to)
        print('Bound and listening')
        self.server.listen(0)

        self.isRunning = True
        self.runSynchronisation()
        return True

    def stop(self):
        print('stop')
        self.isRunning = False
        self.server.shutdown(socket.SHUT_RDWR)
        return True

    def runSynchronisation(self):
        thread = threading.Thread(target = self._acceptConnections)
        thread.start()

    def _readData(self, sock):
        while self.isRunning:
            data = sock.recv(1024)
            if not data:
                break

            if data.startswith('F'):
                freq = int(data[1:].strip())
                if self.cur_freq != freq:
                    if self.verbose:
                        print "New frequency: %d" % freq
                    self.callback(freq)
                    self.cur_freq = freq
                sock.sendall("RPRT 0\n")
            elif data.startswith('f'):
                sock.sendall("f: %d\n" % self.cur_freq)

    def _acceptConnections(self):
        bind_to = (self.gpredict_host, self.gpredict_port)

        while self.isRunning:
            if self.verbose:
                print "Waiting for connection on: %s:%d" % bind_to
            sock, addr = self.server.accept()
            if self.verbose:
                print "Connected from: %s:%d" % (addr[0], addr[1])

            try:
                self._readData(sock)
            except Exception as e:
                print e
            finally:
                sock.close()
            if self.verbose:
                print "Disconnected from: %s:%d" % (addr[0], addr[1])
