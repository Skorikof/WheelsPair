import inspect

import LogPrg
from datetime import datetime
from Settings import DataWheelsRun, DataWheelsGeo, PrgProperties
from Threads import RunSwitchReader, GeoSwitchReader
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThreadPool


class PollSignals(QObject):
    get_Delete_Operator = pyqtSignal()
    get_Delete_Wheels = pyqtSignal()
    get_Prg_Mode = pyqtSignal(str)
    signal_edit_serial = pyqtSignal()
    signal_run_switch = pyqtSignal()
    signal_run_switch_close = pyqtSignal()
    signal_geo_switch = pyqtSignal()
    signal_geo_switch_close = pyqtSignal()
    signalStartRun = pyqtSignal()
    signalStopRun = pyqtSignal()
    signalStartGeo = pyqtSignal()
    signalStopGeo = pyqtSignal()


class PollExchange(object):
    signals = PollSignals()

    def __init__(self, client, win):
        super(PollExchange, self).__init__()
        self.logger = LogPrg.get_logger(__name__)
        self.wheelsRun = DataWheelsRun()
        self.wheelsGeo = DataWheelsGeo()
        self.client = client
        self.win = win

        self.prg = PrgProperties()

        self.threadpool = QThreadPool()

        self.readSwitch()

    def readSwitch(self):
        try:
            self.readerRunSwitch = RunSwitchReader(self.client)
            self.readerRunSwitch.signals.run_switch.connect(self.readSwitchResult)
            self.readerRunSwitch.signals.error_read.connect(self.errorRead)
            self.readerRunSwitch.signals.error_modbus.connect(self.errorModbus)
            self.signals.signal_run_switch.connect(self.readerRunSwitch.startThread)
            self.signals.signal_run_switch_close.connect(self.readerRunSwitch.exitThread)
            self.threadpool.start(self.readerRunSwitch)
            self.readerRunSwitch.startThread()

            self.readerGeoSwitch = GeoSwitchReader(self.client)
            self.readerGeoSwitch.signals.geo_switch.connect(self.readSwitchResult)
            self.readerGeoSwitch.signals.error_read.connect(self.errorRead)
            self.readerGeoSwitch.signals.error_modbus.connect(self.errorModbus)
            self.signals.signal_geo_switch.connect(self.readerGeoSwitch.startThread)
            self.signals.signal_geo_switch_close.connect(self.readerGeoSwitch.exitThread)
            self.threadpool.start(self.readerGeoSwitch)
            self.readerGeoSwitch.startThread()

        except Exception as e:
            self.logger.error(e)

    def readSwitchResult(self, mode, data):
        try:
            if mode == 'run':
                self.run_switch = data

            if mode == 'geo':
                self.geo_swith = data

        except Exception as e:
            self.logger.error(e)



    def btnTestRun(self):
        try:
            if self.prg.query_serial:
                self.signals.signal_edit_serial.emit()
            else:
                self.prg.mode = 'test_run'
                self.signals.get_Prg_Mode.emit('test_run')
                self.win.ui.run_test_repeat_btn.setEnabled(False)
                self.win.ui.run_test_save_btn.setEnabled(False)
                self.fillLineDataRun()
                self.win.ui.stackedWidget.setCurrentIndex(3)

        except Exception as e:
            self.logger.error(e)

    def btnTestGeo(self):
        try:
            if self.prg.query_serial:
                self.signals.signal_edit_serial.emit()
            else:
                self.prg.mode = 'test_geo'
                self.signals.get_Prg_Mode.emit('test_geo')
                self.win.ui.geometry_test_repeat_btn.setEnabled(False)
                self.win.ui.geometry_test_save_btn.setEnabled(False)
                self.win.ui.stackedWidget.setCurrentIndex(5)

        except Exception as e:
            self.logger.error(e)

    def fillLineDataRun(self):
        try:
            self.win.ui.run_test_name_lineEdit.setText(str(self.wheelsRun.name))
            self.win.ui.run_test_serial_lineEdit.setText(str(self.prg.serial_num_run))
            self.win.ui.run_test_gear_lineEdit.setText(str(self.win.prg.type_gear))
            self.win.ui.run_test_direct_lineEdit.setText(str(self.win.prg.direct_run))
            self.win.ui.run_test_time_lineEdit.setText(str(self.wheelsRun.time_test))
            self.win.ui.run_test_oper_lineEdit.setText(str(self.prg.rank + ' ' + self.prg.operator))

            txt_time = str(datetime.now())
            self.prg.date_start_run = txt_time[:-7]
            self.win.ui.run_test_date_lineEdit.setText(self.prg.date_start_run)

        except Exception as e:
            self.logger.error(e)

    def btnOkMessageClicked(self):
        try:
            if self.prg.is_question:
                self.prg.is_question = False
                if self.prg.questionMode == 1:
                    self.win.ui.stackedWidget.setCurrentIndex(1)

                if self.prg.questionMode == 2:
                    self.signals.get_Delete_Operator.emit()

                if self.prg.questionMode == 3:
                    self.signals.get_Delete_Wheels.emit()

            self.win.ui.main_btn_frame.setEnabled(True)

        except Exception as e:
            self.logger.error(e)

    def stopTestBtn(self):
        try:
            if self.prg.mode == 'test_run':
                self.win.ui.run_test_repeat_btn.setEnabled(True)
                self.signals.signalStopRun.connect(self.reader.stopThread)

        except Exception as e:
            self.logger.error(e)

    def repeatTest(self):
        try:
            if self.prg.mode == 'test_run':
                self.btnTestRun()

        except Exception as e:
            self.logger.error(e)

    def resultRead(self, result):
        try:
            print(result)

        except Exception as e:
            self.logger.error(e)

    def errorRead(self, text):
            print(text)

    def errorModbus(self, text):
        print(text)


