#!/usr/bin/env python3

import sys
import signal
import threading
from gnuradio import gr
import signal
from gnuradio import analog, blocks
import bladeRF
import time


class freqpuzzle(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "freqpuzzle", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        samp_rate = 1e6
        freq_start = 100e6
        freq_end = 200e6
        sweep_sec = 30
        sweep_freq = 1/sweep_sec
        scan_samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.bladeRF_source_0 = bladeRF.source(
            args="numchan=" + str(1)
                 + ",metadata=" + 'False'
                 + ",bladerf=" +  str('0')
                 + ",verbosity=" + 'verbose'
                 + ",fpga=" + str('')
                 + ",fpga-reload=" + 'False'
                 + ",ref_clk=" + str(int(0))
                 + ",in_clk=" + 'ONBOARD'
                 + ",out_clk=" + str(False)
                 + ",use_dac=" + 'False'
                 + ",dac=" + str(10000)
                 + ",xb200=" + 'none'
                 + ",tamer=" + 'internal'
                 + ",sampling=" + 'internal'
                 + ",lpf_mode="+'disabled'
                 + ",smb="+str(int(0))
                 + ",dc_calibration="+'LPF_TUNING'
                 + ",trigger0="+'False'
                 + ",trigger_role0="+'master'
                 + ",trigger_signal0="+'J51_1'
                 + ",trigger1="+'False'
                 + ",trigger_role1="+'master'
                 + ",trigger_signal1="+'J51_1'
                 + ",bias_tee0="+'False'
                 + ",bias_tee1="+'False'


        )
        self.bladeRF_source_0.set_sample_rate(samp_rate)
        self.bladeRF_source_0.set_center_freq(freq_start,0)
        self.bladeRF_source_0.set_bandwidth(200000,0)
        self.bladeRF_source_0.set_dc_offset_mode(0, 0)
        self.bladeRF_source_0.set_iq_balance_mode(0, 0)
        self.bladeRF_source_0.set_gain_mode(False, 0)
        self.bladeRF_source_0.set_gain(10, 0)
        self.bladeRF_source_0.set_if_gain(20, 0)

        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self.analog_sig_source_x_0 = analog.sig_source_f(
            scan_samp_rate, analog.GR_SAW_WAVE, sweep_freq, 1, 0, 0)
        self.blocks_throttle_0 = blocks.throttle(
            gr.sizeof_float*1, scan_samp_rate, True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(
            freq_end-freq_start)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(freq_start)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.bladeRF_source_0, 0), (self.blocks_null_sink_0, 0))

        self.connect((self.analog_sig_source_x_0, 0),
                     (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0),
                     (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0),
                     (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0),
                     (self.blocks_probe_signal_x_0, 0))

        def _center_freq_probe():
            while True:
                val = self.blocks_probe_signal_x_0.level()
                if not val:
                    continue
                self.bladeRF_source_0.set_center_freq(val, 0)
                get_val = self.bladeRF_source_0.get_center_freq(0)
                if val != get_val:
                    print(f'wanted {val} got {get_val} ({get_val - val})')
                time.sleep(1.0 / (99.7))

        self.center_freq_thread = threading.Thread(target=_center_freq_probe)
        self.center_freq_thread.daemon = True
        self.center_freq_thread.start()


def main(top_block_cls=freqpuzzle, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
