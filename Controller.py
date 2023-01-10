import LogPrg
import sys
import View
from Polls import PollExchange
import Settings
import GlobalVar
from PyQt5.QtWidgets import QApplication


class Controller(object):
    prg = Settings.PrgProperties()

    def __init__(self):
        super(Controller, self).__init__()

        self.logger = LogPrg.get_logger(__name__)

        self.set_port = Settings.PortSettings()
        self.window = View.ChangeUI()

        self.winConnection()

        self.exchange = PollExchange(self.set_port.client, self.window)

    def winConnection(self):
        try:
            self.window.signals.app_quit.connect(self.closePrg)
            self.window.signals.get_questions.connect(self.winQuestions)
            self.window.signals.get_operator.connect(self.setOperator)
            self.window.signals.get_wheelRun.connect(self.setWheelsRun)
            self.window.signals.get_wheelGeo.connect(self.setWheelsGeo)

        except Exception as e:
            self.logger.error(e)

    def winQuestions(self, mode):
        try:
            self.prg.questionMode = mode
            self.exchange.prg.questionMode = mode
            self.prg.is_question = True
            self.exchange.prg.is_question = True

            self.window.ui.msg_ok_btn.setVisible(True)
            self.window.ui.msg_cancel_btn.setVisible(True)
            self.window.ui.main_btn_frame.setEnabled(False)
            self.window.ui.stackedWidget.setCurrentIndex(0)

            self.window.ui.msg_label.setStyleSheet("background-color: " + GlobalVar.COLOR_ORANGE +
                                                   ";\n" + "color: " + GlobalVar.COLOR_BLACK + ";")

            if mode == 1: #Если ввели совпадение при вводе оператора или колёсной пары
                self.window.ui.msg_label.setText('Введенные данные\nуже содержатся в списке...')
                self.window.ui.msg_ok_btn.setVisible(False)


            if mode == 2: # Вопрос при удалении оператора
                self.window.ui.msg_label.setText('Удалить выбранного оператора\n'
                                                 + self.window.operators.names[
                                                  self.window.operators.current_index] + ' ?')

            if mode == 3: # Вопрос про удаление колёсной пары
                if self.prg.mode == 'run':
                    self.window.ui.msg_label.setText('Удалить выбранную\nколёсную пару\n'
                                 + self.window.wheels.struct.wheelsRun[self.window.wheels.current_index_run].name + ' ?')
                if self.prg.mode == 'geo':
                    self.window.ui.msg_label.setText('Удалить выбранную\nколёсную пару\n'
                                 + self.window.wheels.struct.wheelsGeo[self.window.wheels.current_index_geo].name + ' ?')

        except Exception as e:
            self.logger.error(e)

    def threadConnection(self):
        try:
            self.exchange.signals.get_Delete_Operator.connect(self.deleteOperator)
            self.exchange.signals.get_Delete_Wheels.connect(self.deleteWheels)

            self.window.ui.msg_ok_btn.clicked.connect(self.exchange.btnOkMessageClicked)
            self.window.ui.msg_cancel_btn.clicked.connect(self.btnCancelMsgClick)

            self.window.ui.main_operator_btn.clicked.connect(self.btnMainOperator)
            self.window.ui.main_run_btn.clicked.connect(self.btnMainWheelsRun)
            self.window.ui.main_geometry_btn.clicked.connect(self.btnMainWheelsGeo)
            self.window.ui.main_hand_debug_btn.clicked.connect(self.btnMainDebug)

            self.window.ui.run_continue_btn.clicked.connect(self.exchange.btnTestRun)
            self.window.ui.run_test_cancel_btn.clicked.connect(self.stopBtn)
            self.window.ui.geometry_continue_btn.clicked.connect(self.exchange.btnTestGeo)

            self.exchange.signals.signal_edit_serial.connect(self.setSerialNumber)
            self.window.keyboardS.signals.finished_serial_number.connect(self.serialNumberFromKeyb)

        except Exception as e:
            self.logger.error(e)

    def setSerialNumber(self):
        try:
            self.window.keyboardS.mode_edit = 1
            self.window.setEnabled(False)
            self.window.keyboardS.type_keyb = 'serial'
            self.window.keyboardS.InitKeys()
            self.window.keyboardS.setVisible(True)

        except Exception as e:
            self.logger.error(e)

    def serialNumberFromKeyb(self, ser_n):
        try:
            self.window.setEnabled(True)
            self.window.keyboardS.setVisible(False)
            self.exchange.prg.query_serial = False
            if self.prg.mode == 'run':
                self.exchange.prg.serial_num_run = ser_n
                self.exchange.btnTestRun()
            if self.prg.mode == 'geo':
                self.exchange.prg.serial_num_geo = ser_n
                self.exchange.btnTestGeo()

        except Exception as e:
            self.logger.error(e)

    def setOperator(self, name, rank):
        try:
            self.prg.operator = name
            self.exchange.prg.operator = name
            self.prg.rank = rank
            self.exchange.prg.rank = rank
            self.window.selectedName = name
            self.window.lbl_info_Operator.setText('Оператор: {0} {1}'.format(self.prg.rank,
                                                                             self.prg.operator))
        except Exception as e:
            self.logger.error(e)

    def deleteOperator(self):
        try:
            if len(self.window.operators.names) == 0 or self.window.selectedName == self.prg.operator:
                self.prg.operator = ''
                self.prg.rank = ''
                self.window.selectedName = ''
                self.window.lbl_info_Operator.setText('Оператор:')

            self.window.operators.deleteOperator(self.window.operators.current_index)
            self.window.updateOperators()
            self.window.ui.stackedWidget.setCurrentIndex(1)
            self.window.ui.main_btn_frame.setEnabled(True)

        except Exception as e:
            self.logger.error(e)

    def btnMainOperator(self):
        try:
            self.prg.mode = 'operators'
            self.window.ui.stackedWidget.setCurrentIndex(1)

        except Exception as e:
            self.logger.error(e)

    def btnMainWheelsRun(self):
        try:
            self.prg.mode = 'run'
            self.exchange.prg.mode = 'run'
            self.exchange.prg.query_serial = True
            self.window.ui.stackedWidget.setCurrentIndex(2)
            self.window.initWheels('run')

        except Exception as e:
            self.logger.error(e)

    def btnMainWheelsGeo(self):
        try:
            self.prg.mode = 'geo'
            self.exchange.prg.mode = 'geo'
            self.exchange.prg.query_serial = True
            self.window.ui.stackedWidget.setCurrentIndex(4)
            self.window.initWheels('geo')

        except Exception as e:
            self.logger.error(e)

    def btnMainDebug(self):
        try:
            self.prg.mode = 'debug'
            self.window.ui.stackedWidget.setCurrentIndex(6)

        except Exception as e:
            self.logger.error(e)

    def setWheelsRun(self, obj):
        try:
            self.exchange.wheelsRun = obj

        except Exception as e:
            self.logger.error(e)

    def setWheelsGeo(self, obj):
        try:
            self.exchange.wheelsGeo = obj

        except Exception as e:
            self.logger.error(e)

    def deleteWheels(self):
        try:
            if self.prg.mode == 'run':
                self.window.wheels.deleteWheels(self.window.wheels.current_index_run)
                self.window.ui.stackedWidget.setCurrentIndex(2)
            if self.prg.mode == 'geo':
                self.window.wheels.deleteWheels(self.window.wheels.current_index_geo)
                self.window.ui.stackedWidget.setCurrentIndex(4)
            self.window.ui.main_btn_frame.setEnabled(True)
            self.window.updateWheels()

        except Exception as e:
            self.logger.error(e)

    def btnCancelMsgClick(self):
        try:
            if self.prg.mode == 'operators':
                self.window.ui.stackedWidget.setCurrentIndex(1)

            if self.prg.mode == 'run':
                self.window.ui.stackedWidget.setCurrentIndex(2)

            if self.prg.mode == 'geo':
                self.window.ui.stackedWidget.setCurrentIndex(4)
            self.window.ui.main_btn_frame.setEnabled(True)

        except Exception as e:
            self.logger.error(e)

    def stopBtn(self):
        try:
            self.exchange.stopTestBtn()

        except Exception as e:
            self.logger.error(e)

    def closePrg(self):
        try:
            self.exchange.signals.signal_run_switch_close.emit()
            self.exchange.signals.signal_geo_switch_close.emit()
            self.logger.info('Programm is exit')
            self.window.close()
            self.set_port.client.close()

        except Exception as e:
            self.logger.error(e)


def main():
    logger = LogPrg.get_logger(__name__)
    try:
        logger.info('Starting the programm')
        app = QApplication(sys.argv)
        app_control = Controller()
        app_control.threadConnection()

        app_control.window.show()
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(e)


if __name__=='__main__':
    main()

