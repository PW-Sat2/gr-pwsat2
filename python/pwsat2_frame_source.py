import numpy
from gnuradio import gr
import collections
import pmt
import array
import zmq
import thread


class pwsat2_frame_source(gr.basic_block):
    """
    docstring for block hdlc_framer
    """
    def __init__(self, address, isBound):
        gr.basic_block.__init__(self,
            name="pwsat2_frame_source",
            in_sig=None,
            out_sig=None)

        self.address = address
        self.message_port_register_out(pmt.intern('out'))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        if isBound:
            self.socket.bind(address)
        else:
            self.socket.connect(address)
            
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

        thread.start_new_thread(self.loop, ())

    def loop(self):
        while True:
            if self.socket.poll(timeout=1) > 0:
                buff = self.socket.recv()
                buff = [ord(i) for i in buff]

                pkt = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(buff), buff))

                self.message_port_pub(pmt.intern('out'), pkt)
