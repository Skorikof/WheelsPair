import time
from struct import pack, unpack
import LogPrg
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, QTimer
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class ReaderSignals(QObject):
    result = pyqtSignal(object)
    error_read = pyqtSignal(object)

class Reader(QRunnable):
    signals = ReaderSignals()
    def __init__(self, id, client):
        super(Reader, self).__init__()
        self.logger = LogPrg.get_logger(__name__)

        self.cycle = True

        self.ID = id
        self.client = client

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    rr = 'Run is running'
                    self.signals.result.emit(rr)
                    # if rr:
                    #     self.signals.result.emit(rr)
                    # else:
                    #     self.signals.error_read.emit(rr)

            except Exception as e:
                self.logger.error(e)


    def startThread(self):
        self.is_run = True

    def stopThread(self):
        self.is_run = False

    def exitThread(self):
        try:
            self.cycle = False

        except Exception as e:
            self.logger.error(e)

    def setStatePrg(self, val_state):
        try:
            self.value_state_prg = val_state
            self.query_change_state = True

        except Exception as e:
            self.logger.error(e)

    def setModePrg(self, val_mode):
        try:
            self.val_mode = val_mode
            self.query_change_mode = True

        except Exception as e:
            self.logger.error(e)

    def inverseBit(self, val_bit):
        try:
            temp_b = 0
            if val_bit == 0:
                temp_b = 1
            return temp_b

        except Exception as e:
            self.logger.error(e)

    def decToBinStr(self, val_d):
        try:
            bin_str = bin(val_d)
            bin_str = bin_str[2:]
            bin_str = bin_str.zfill(16)
            bin_str = ''.join(reversed(bin_str))
            bin_list = []
            for i in bin_str:
                bin_list.append(int(i))
            return bin_list

        except Exception as e:
            self.logger.error(e)
