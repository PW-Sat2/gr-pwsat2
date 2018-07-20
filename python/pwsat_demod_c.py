# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: PW-Sat2 Demodulator
# Generated: Fri Jul 20 12:49:32 2018
# GNU Radio version: 3.7.12.0
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
import satellites
import sip


class pwsat_demod_c(gr.hier_block2, Qt.QWidget):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "PW-Sat2 Demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out("frames")

        Qt.QWidget.__init__(self)
        self.top_layout = Qt.QVBoxLayout()
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.setLayout(self.top_layout)

        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 1200
        self.samp_per_sym = samp_per_sym = 10
        self.samp_rate = samp_rate = symb_rate*samp_per_sym
        self.frequency_offset = frequency_offset = -20e3
        self.decimation = decimation = 16

        self.bpsk = bpsk = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()

        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################
        self._frequency_offset_range = Range(-40e3, 40e3, 10, -20e3, 200)
        self._frequency_offset_win = RangeWidget(self._frequency_offset_range, self.set_frequency_offset, 'Frequency Offset', "counter_slider", float)
        self.top_grid_layout.addWidget(self._frequency_offset_win)
        self._decimation_options = (16, 8, 4, 2, )
        self._decimation_labels = ('1200', '2400', '4800', '9600', )
        self._decimation_tool_bar = Qt.QToolBar(self)
        self._decimation_tool_bar.addWidget(Qt.QLabel('Symbol Rate'+": "))
        self._decimation_combo_box = Qt.QComboBox()
        self._decimation_tool_bar.addWidget(self._decimation_combo_box)
        for label in self._decimation_labels: self._decimation_combo_box.addItem(label)
        self._decimation_callback = lambda i: Qt.QMetaObject.invokeMethod(self._decimation_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._decimation_options.index(i)))
        self._decimation_callback(self.decimation)
        self._decimation_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_decimation(self._decimation_options[i]))
        self.top_grid_layout.addWidget(self._decimation_tool_bar)
        self._alpha_range = Range(0, 1, 1e-3, 0.5, 200)
        self._alpha_win = RangeWidget(self._alpha_range, self.set_alpha, "alpha", "counter_slider", float)
        self.top_grid_layout.addWidget(self._alpha_win)
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, samp_rate, symb_rate, alpha, 300))
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	192000, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	192000, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	128, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.low_pass(1, 192000, 40000, 1000)), frequency_offset, 192000)
        self.fractional_resampler_xx_0 = filter.fractional_resampler_cc(0, decimation)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(digital.TED_ZERO_CROSSING, samp_per_sym, 0.045, 1.0, 1, 0.1, 1, digital.constellation_bpsk().base(), digital.IR_MMSE_8TAP, 128, ([]))
        self.digital_descrambler_bb_0_1 = digital.descrambler_bb(0x21, 0x00, 16)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(0.1, 2, False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.analog_agc_xx_0 = analog.agc_cc(1e-3, 1, 1.0)
        self.analog_agc_xx_0.set_max_gain(30)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self, 'frames'))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_descrambler_bb_0_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.digital_descrambler_bb_0_1, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.fractional_resampler_xx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fractional_resampler_xx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.satellites_hdlc_deframer_0, 0))

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samp_rate(self.symb_rate*self.samp_per_sym)
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, self.alpha, 300))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_samp_rate(self.symb_rate*self.samp_per_sym)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, self.alpha, 300))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_frequency_offset(self):
        return self.frequency_offset

    def set_frequency_offset(self, frequency_offset):
        self.frequency_offset = frequency_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.frequency_offset)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self._decimation_callback(self.decimation)
        self.fractional_resampler_xx_0.set_resamp_ratio(self.decimation)

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, self.alpha, 300))
