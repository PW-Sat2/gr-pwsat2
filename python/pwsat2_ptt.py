import numpy
from gnuradio import gr
import serial
from threading import Timer

class pwsat2_ptt(gr.sync_block):
    """
    docstring for block pwsat2_ptt
    """
    def __init__(self, device, baudrate, samp_rate, delay):
        gr.sync_block.__init__(self,
            name="pwsat2_ptt",
            in_sig=[numpy.float32],
            out_sig=None)

        self.ptt = serial.Serial()
        self.device = device
        self.baudrate = baudrate
        self.samp_rate = samp_rate
        self.delay = delay
        self.timer = None

    def start(self):
        try:
            self.ptt.rts = False
            self.ptt.baudrate = self.baudrate
            self.ptt.port = self.device
            self.ptt.open()
            return True 
        except:
            return False
        
    def stop(self):
        self.ptt.close()
        return True

    def stop_tx(self):
        self.ptt.rts = False

    def work(self, input_items, output_items):
        self.ptt.rts = True
        if self.timer:
            self.timer.cancel()

        length = len(input_items[0])
        time_of_packet = float(length) / float(self.samp_rate)
        total_time = time_of_packet + self.delay
        self.timer = Timer(total_time, self.stop_tx)
        self.timer.start()

        return length

