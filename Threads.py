import time
from struct import pack, unpack
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, QTimer
from pymodbus.exceptions import ModbusException as ModEx


class ReaderSignals(QObject):
    log_result = pyqtSignal(object)
    run_switch = pyqtSignal(str, object)
    run_switch_read = pyqtSignal(str, bool)
    geo_switch = pyqtSignal(str, object)
    geo_switch_read = pyqtSignal(str, bool)
    error_read = pyqtSignal(object)
    error_modbus = pyqtSignal(object)


class RunSwitchReader(QRunnable):
    signals = ReaderSignals()

    def __init__(self, client):
        super(RunSwitchReader, self).__init__()
        self.cycle = True
        self.client = client
        self.run_switch_bool = False
        self.run_switch_str = '1111111111111111'

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    # rr = self.client.read_holding_registers(51, 1, unit=36)
                    # if not rr.isError():
                    #     self.run_switch_bool = True
                    #     result = str(bin(rr.registers[0])[2:].zfill(16))[::-1]
                    #     self.signals.run_switch.emit('run', result)
                    #
                    # else:
                    #     self.run_switch_bool = False

                    self.signals.run_switch.emit('run', self.run_switch_str)
                    time.sleep(1)

            except ModEx as e:
                text = 'Read switch RUN ' + str(e)
                self.signals.error_modbus.emit(text)
                time.sleep(1)

            except Exception as e:
                self.signals.error_read.emit(e)


    def startThread(self):
        self.is_run = True

    def exitThread(self):
        try:
            self.cycle = False

        except Exception as e:
            self.signals.error_read.emit(e)


class GeoSwitchReader(QRunnable):
    signals = ReaderSignals()

    def __init__(self, client):
        super(GeoSwitchReader, self).__init__()
        self.cycle = True
        self.client = client
        self.geo_switch_bool = False
        self.geo_switch_str = '1111111111111111'

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    # rr = self.client.read_holding_registers(51, 1, unit=4)
                    # if not rr.isError():
                    #     self.geo_switch_bool = True
                    #     result = str(bin(rr.registers[0])[2:].zfill(16))[::-1]
                    #     self.signals.geo_switch.emit('geo', result)
                    #
                    # else:
                    #     self.geo_switch_bool = False

                    self.signals.geo_switch.emit('geo', self.geo_switch_str)
                    time.sleep(1)

            except ModEx as e:
                text = 'Read switch GEO ' + str(e)
                self.signals.error_modbus.emit(text)
                time.sleep(1)

            except Exception as e:
                self.signals.error_read.emit(e)

    def startThread(self):
        self.is_run = True

    def exitThread(self):
        try:
            self.cycle = False

        except Exception as e:
            self.signals.error_read.emit(e)
