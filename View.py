import sys
import traceback

import GlobalVar
import LogPrg
from MainUi import Ui_MainWindow
from ArchiveRun import RunArchive
from ArchiveGeo import GeoArchive
from Operators import Operators
from KeyString import KeyS
import pyqtgraph as pg
from PIL import ImageGrab
from Settings import PrgProperties, DataWheelsRun, DataWheelsGeo
from Wheels import Wheels

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QFont


class WindowSignals(QObject):
    app_quit = pyqtSignal()
    get_questions = pyqtSignal(int)
    get_operator = pyqtSignal(str, str)
    get_wheelRun = pyqtSignal(object)
    get_wheelGeo = pyqtSignal(object)


class ChangeUI(QMainWindow):
    prg = PrgProperties()

    def __init__(self):
        super(ChangeUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(0)

        self.signals = WindowSignals()

        self.logger = LogPrg.get_logger(__name__)

        fg = self.frameGeometry()
        self.keyboardS = KeyS(fg)

        self.winConnection()
        self.initStatusBar()
        self.initOperators()
        self.initDebug()

        self.new_name = ''
        self.new_rank = ''
        self.selectedName = ''
        self.new_wheelsRun = DataWheelsRun()
        self.current_wheelsRun = DataWheelsRun()
        self.new_wheelsGeo = DataWheelsGeo()
        self.current_wheelsGeo = DataWheelsGeo()

        self.ui.msg_ok_btn.setVisible(False)
        self.ui.msg_cancel_btn.setVisible(False)

    def winConnection(self):
        try:
            self.ui.main_close_btn.clicked.connect(self.queryClose)

            self.ui.operator_ok_btn.clicked.connect(self.btnOkOperatorClick)
            self.ui.operator_add_btn.clicked.connect(self.btnAddOperatorClick)
            self.ui.operator_del_btn.clicked.connect(self.btnDelOperatorClick)

            self.ui.run_del_btn.clicked.connect(self.btnDelWheelsClick)
            self.ui.run_add_btn.clicked.connect(self.btnAddWheelClick)
            self.ui.geometry_del_btn.clicked.connect(self.btnDelWheelsClick)
            self.ui.geometry_add_btn.clicked.connect(self.btnAddWheelClick)

            self.keyboardS.signals.finished.connect(self.addOperator)
            self.keyboardS.signals.finished_wheelRun.connect(self.addWheels)
            self.keyboardS.signals.finished_wheelGeo.connect(self.addWheels)
            self.keyboardS.signals.cancel_edit.connect(self.cancelAddOperator)

            self.ui.main_archive_btn.clicked.connect(self.archive_page)

            self.ui.run_direct_comboBox.clear()
            self.ui.run_debug_direct_comboBox.clear()
            temp_direct = ['Прямое', 'Реверс', 'Прямое и Реверс']
            self.ui.run_direct_comboBox.addItems(temp_direct)
            self.ui.run_debug_direct_comboBox.addItems(temp_direct)
            self.directWheelsRun(0)

            self.ui.run_type_gear_comboBox.clear()
            self.ui.run_debug_gear_comboBox.clear()
            temp_gear = ['Кардан 1', 'Кардан 2', 'Ролик']
            self.ui.run_type_gear_comboBox.addItems(temp_gear)
            self.ui.run_debug_gear_comboBox.addItems(temp_gear)
            self.typeGearWheelsRun(0)

            self.ui.run_type_carrier_comboBox.clear()
            temp_carrier = ['Положение 1', 'Положение 2', 'Положение 3']
            self.ui.run_type_carrier_comboBox.addItems(temp_carrier)
            self.typeCarrierWheelsRun(0)

            self.ui.geometry_count_test_comboBox.clear()
            for i in range(1, 11):
                temp_count = str(i)
                self.ui.geometry_count_test_comboBox.addItem(temp_count)
            self.count_testGeo(0)

        except Exception as e:
            self.logger.error(e)

    def initStatusBar(self):
        try:
            self.lbl_info_Operator = QLabel('Оператор:')
            self.lbl_info_Operator.setStyleSheet('border: 0; color: black;')
            self.lbl_info_Operator.setFont(QFont('Calibri', 14))

            self.statusBar().addPermanentWidget(self.lbl_info_Operator, stretch = 1)

        except Exception as e:
            self.logger.error(e)

    def initOperators(self):
        try:
            self.operators = Operators()
            self.updateOperators()
            self.prg.set_operator = False

        except Exception as e:
            self.logger.error(e)

    def initWheels(self, mode):
        try:
            if mode == 'run':
                self.prg.type_wheel = 'run'
            if mode == 'geo':
                self.prg.type_wheel = 'geo'

            self.wheels = Wheels(self.prg)
            self.updateWheels()

        except Exception as e:
            self.logger.error(e)

    def initDebug(self):
        try:
            self.ui.debug_run_frame.setEnabled(True)
            self.ui.debug_geometry_frame.setEnabled(True)

            if self.prg.test_run:
                self.ui.debug_run_frame.setEnabled(False)
            if self.prg.test_geo:
                self.ui.debug_geometry_frame.setEnabled(False)

            self.hand_debug_page()

        except Exception as e:
            self.logger.error(e)

    def updateOperators(self):
        try:
            self.operators.updateOperatorsList()
            self.ui.main_btn_frame.setEnabled(True)
            self.ui.operator_ok_btn.setEnabled(True)
            self.ui.operator_del_btn.setEnabled(True)
            self.ui.oper_name_comboBox.clear()
            self.ui.oper_rank_lineEdit.clear()
            self.ui.oper_rank_lineEdit.setReadOnly(True)

            if len(self.operators.config.sections()) == 0:
                self.ui.operator_ok_btn.setEnabled(False)
                self.ui.operator_del_btn.setEnabled(False)

            else:
                self.ui.oper_name_comboBox.addItems(self.operators.names)
                self.ui.oper_name_comboBox.setCurrentIndex(0)
                self.selectOperatorName(0)
                self.ui.oper_name_comboBox.activated[int].connect(self.selectOperatorName)

        except Exception as e:
            self.logger.error(e)

    def selectOperatorName(self, ind):
        try:
            self.operators.current_index = ind
            self.selectedName = self.operators.names[ind]
            self.ui.oper_rank_lineEdit.setText(self.operators.ranks[ind])
            self.ui.operator_ok_btn.setEnabled(True)
            self.ui.operator_del_btn.setEnabled(True)

        except Exception as e:
            self.logger.error(e)

    def btnOkOperatorClick(self):
        try:
            self.signals.get_operator.emit(self.operators.names[self.operators.current_index],
                                           self.operators.ranks[self.operators.current_index])

            txt_log = 'OPERATOR ' + self.operators.ranks[self.operators.current_index] + ' ' \
            + self.operators.names[self.operators.current_index] + ' is SELECT'

            self.logger.info(txt_log)
            self.prg.set_operator = True
            self.ui.operator_ok_btn.setEnabled(False)

        except Exception as e:
            self.logger.error(e)

    def btnAddOperatorClick(self):
        try:
            self.keyboardS.mode_edit = 1
            self.setEnabled(False)
            self.keyboardS.type_keyb = 'operators'
            self.keyboardS.InitKeys()
            self.keyboardS.setVisible(True)

        except Exception as e:
            self.logger.error(e)

    def addOperator(self, name, rank):
        try:
            self.setEnabled(True)
            self.keyboardS.setVisible(False)
            self.new_name = name
            self.new_rank = rank

            self.checkConcurrenceName(self.new_name, self.new_rank)

        except Exception as e:
            self.logger.error(e)

    def checkConcurrenceName(self, name, rank):
        try:
            flag = False
            for oper_name in self.operators.names:
                if oper_name.upper() == name.upper():
                    flag = True

            if flag:
                self.signals.get_questions.emit(1)

            else:
                self.operators.addNewOperator(name, rank)
                self.updateOperators()

        except Exception as e:
            self.logger.error(e)

    def cancelAddOperator(self):
        try:
            self.setEnabled(True)
            self.keyboardS.setVisible(False)

        except Exception as e:
            self.logger.error(e)

    def btnDelOperatorClick(self):
        try:
            self.signals.get_questions.emit(2)

        except Exception as e:
            self.logger.error(e)

    def updateWheels(self):
        try:
            if self.prg.type_wheel == 'run':
                self.ui.run_type_pair_comboBox.clear()
                self.ui.run_speed_lineEdit.clear()
                self.ui.run_maxtemp_lineEdit.clear()
                self.ui.run_time_lineEdit.clear()
                self.wheels.updateWheelsList()
                self.ui.run_del_btn.setEnabled(True)

                if len(self.wheels.struct.wheelsRun) == 0:
                    self.ui.run_del_btn.setEnabled(False)
                    self.ui.run_continue_btn.setEnabled(False)

                else:
                    for i in self.wheels.struct.wheelsRun:
                        self.ui.run_type_pair_comboBox.addItem(i.name)
                        self.ui.run_type_pair_comboBox.setCurrentIndex(0)
                        self.wheels.current_index_run = 0
                        self.selectWheels(self.wheels.current_index_run)
                        self.ui.run_type_pair_comboBox.activated[int].connect(self.selectWheels)
                        self.ui.run_direct_comboBox.activated[int].connect(self.directWheelsRun)
                        self.ui.run_type_gear_comboBox.activated[int].connect(self.typeGearWheelsRun)
                        self.ui.run_type_carrier_comboBox.activated[int].connect(self.typeCarrierWheelsRun)

            if self.prg.type_wheel == 'geo':
                self.ui.geometry_type_pair_comboBox.clear()
                self.ui.geometry_diameter_lineEdit.clear()
                self.ui.geometry_beat_lineEdit.clear()
                self.ui.geometry_diff_diameter_lineEdit.clear()
                self.ui.geometry_interband_lineEdit.clear()
                self.ui.geometry_unparallel_lineEdit.clear()
                self.ui.geometry_crest_high_lineEdit.clear()
                self.ui.geometry_crest_width_lineEdit.clear()
                self.ui.geometry_crest_diff_lineEdit.clear()
                self.ui.geometry_roll_circle_lineEdit.clear()
                self.ui.geometry_width_rim_lineEdit.clear()
                self.ui.geometry_one_slope_lineEdit.clear()
                self.ui.geometry_two_slope_lineEdit.clear()
                self.wheels.updateWheelsList()
                self.ui.geometry_del_btn.setEnabled(True)
                if len(self.wheels.struct.wheelsGeo) == 0:
                    self.ui.geometry_continue_btn.setEnabled(False)
                    self.ui.geometry_del_btn.setEnabled(False)
                else:
                    for i in self.wheels.struct.wheelsGeo:
                        self.ui.geometry_type_pair_comboBox.addItem(i.name)
                        self.ui.geometry_type_pair_comboBox.setCurrentIndex(0)
                        self.wheels.current_index_geo = 0
                        self.selectWheels(self.wheels.current_index_geo)
                        self.ui.geometry_type_pair_comboBox.activated[int].connect(self.selectWheels)
                        #self.ui.geometry_count_test_comboBox.activated[int].connect(self.count_testGeo)

        except Exception as e:
            self.logger.error(e)

    def selectWheels(self, ind):
        try:
            if self.prg.type_wheel == 'run':
                self.wheels.current_index_run = ind
                self.ui.run_speed_lineEdit.setText(str(self.wheels.struct.wheelsRun[ind].speed))
                self.ui.run_maxtemp_lineEdit.setText(str(self.wheels.struct.wheelsRun[ind].max_temp))
                self.ui.run_time_lineEdit.setText(str(self.wheels.struct.wheelsRun[ind].time_test))

                self.current_wheelsRun = self.wheels.struct.wheelsRun[ind]
                self.signals.get_wheelRun.emit(self.current_wheelsRun)
                if not self.prg.set_operator:
                    self.ui.run_continue_btn.setEnabled(False)
                else:
                    self.ui.run_continue_btn.setEnabled(True)

            if self.prg.type_wheel == 'geo':
                self.wheels.current_index_geo = ind
                self.ui.geometry_diameter_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].diameter))
                self.ui.geometry_beat_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].beat))
                self.ui.geometry_diff_diameter_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].diff_diameter))
                self.ui.geometry_interband_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].interband))
                self.ui.geometry_unparallel_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].unparallel))
                self.ui.geometry_crest_high_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].crest_high))
                self.ui.geometry_crest_width_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].crest_width))
                self.ui.geometry_crest_diff_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].crest_diff))
                self.ui.geometry_roll_circle_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].roll_circle))
                self.ui.geometry_width_rim_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].width_rim))
                self.ui.geometry_one_slope_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].one_slope))
                self.ui.geometry_two_slope_lineEdit.setText(str(self.wheels.struct.wheelsGeo[ind].two_slope))

                self.current_wheelsGeo = self.wheels.struct.wheelsGeo[ind]
                self.signals.get_wheelGeo.emit(self.current_wheelsGeo)
                if not self.prg.set_operator:
                    self.ui.geometry_continue_btn.setEnabled(False)
                else:
                    self.ui.geometry_continue_btn.setEnabled(True)

        except Exception as e:
            self.logger.error(e)

    def directWheelsRun(self, direct):
        try:
            if direct == 0:
                self.prg.direct_run = 'Прямое'
            if direct == 1:
                self.prg.direct_run = 'Реверс'
            if direct == 2:
                self.prg.direct_run = 'Прямое и Реверс'

        except Exception as e:
            self.logger.error(e)

    def typeGearWheelsRun(self, gear):
        try:
            if gear == 0:
                self.prg.type_gear = 'Кардан 1'
            if gear == 1:
                self.prg.type_gear = 'Кардан 2'
            if gear == 2:
                self.prg.type_gear = 'Ролик'

        except Exception as e:
            self.logger.error(e)

    def typeCarrierWheelsRun(self, carrier):
        try:
            if carrier == 0:
                self.prg.type_carrier = 'Положение 1'
            if carrier == 1:
                self.prg.type_carrier = 'Положение 2'
            if carrier == 2:
                self.prg.type_carrier = 'Положение 3'

        except Exception as e:
            self.logger.error(e)

    def count_testGeo(self, count):
        try:
            self.prg.count_testGeo = count + 1

        except Exception as e:
            self.logger.error(e)

    def btnAddWheelClick(self):
        try:
            if self.prg.type_wheel == 'run':
                self.keyboardS.type_keyb = 'wheels_run'
            if self.prg.type_wheel == 'geo':
                self.keyboardS.type_keyb = 'wheels_geo'
            self.keyboardS.mode_edit = 1
            self.setEnabled(False)
            self.keyboardS.InitKeys()
            self.keyboardS.setVisible(True)

        except Exception as e:
            self.logger.error(e)

    def addWheels(self, obj):
        try:
            self.setEnabled(True)
            self.keyboardS.setVisible(False)
            if self.prg.type_wheel == 'run':
                self.new_wheelsRun = obj
                self.checkConcurrenceWheel(self.new_wheelsRun)
            if self.prg.type_wheel == 'geo':
                self.new_wheelsGeo = obj
                self.checkConcurrenceWheel(self.new_wheelsGeo)

        except Exception as e:
            self.logger.error(e)

    def checkConcurrenceWheel(self, obj):
        try:
            flag_c = False
            if self.prg.type_wheel == 'run':
                for i in range(len(self.wheels.struct.wheelsRun)):
                    if obj.name.upper() == self.wheels.struct.wheelsRun[i].name.upper():
                        flag_c = True

                if flag_c:
                    self.signals.get_questions.emit(1)

                else:
                    self.wheels.addNewWheels(obj)
                    self.updateWheels()

            if self.prg.type_wheel == 'geo':
                for i in range(len(self.wheels.struct.wheelsGeo)):
                    if obj.name.upper() == self.wheels.struct.wheelsGeo[i].name.upper():
                        flag_c = True

                if flag_c:
                    self.signals.get_questions.emit(1)

                else:
                    self.wheels.addNewWheels(obj)
                    self.updateWheels()

        except Exception as e:
            self.logger.error(e)

    def btnDelWheelsClick(self):
        try:
            self.signals.get_questions.emit(3)

        except Exception as e:
            self.logger.error(e)

    def hand_debug_page(self):
        pass

    def archive_page(self):
        try:
            self.archiveRun = RunArchive()
            self.archiveGeo = GeoArchive()

            self.ui.stackedWidget.setCurrentIndex(7)
            self.ui.archive_test_comboBox.clear()
            self.ui.archive_test_comboBox.addItem('Обкатка')
            self.ui.archive_test_comboBox.addItem('Геометрия')
            self.archive_process(0)
            self.ui.archive_test_comboBox.activated[int].connect(self.archive_process)

        except Exception as e:
            self.logger.error(e)

    def archive_process(self, test):
        try:
            if test == 0:
                self.name_test = 'run'
                self.archive_test()
            if test == 1:
                self.name_test = 'geo'
                self.archive_test()

        except Exception as e:
            self.logger.error(e)

    def archive_test(self):
        try:
            self.ui.archive_date_comboBox.clear()
            self.ui.archive_time_comboBox.clear()

            if self.name_test == 'run':
                self.archiveRun.init_arch()
                self.ui.stackedWidget_archive.setCurrentIndex(0)

                for i in range(len(self.archiveRun.files_name_arr)):
                    self.ui.archive_date_comboBox.addItem(self.archiveRun.files_name_sort[i])

                self.archive_date(self.archiveRun.files_name_sort[0])
                self.ui.archive_date_comboBox.activated[str].connect(self.archive_date)

            if self.name_test == 'geo':
                self.archiveGeo.init_arch()
                self.ui.stackedWidget_archive.setCurrentIndex(1)

                self.ui.archive_angle_comboBox.clear()

                for i in range(len(self.archiveGeo.files_name_arr)):
                    self.ui.archive_date_comboBox.addItem((self.archiveGeo.files_name_sort[i]))

                self.archive_date(self.archiveGeo.files_name_sort[0])
                self.ui.archive_date_comboBox.activated[str].connect(self.archive_date)

        except Exception as e:
            self.logger.error(e)

    def archive_date(self, date):
        try:
            self.ui.archive_time_comboBox.clear()
            if self.name_test == 'run':
                temp_arr = []
                self.archiveRun.select_file(date)
                self.date_select_archive_run = self.archiveRun.files_name_arr[self.archiveRun.index_archive]

                for i in range(len(self.archiveRun.struct.tests)):
                    temp = self.archiveRun.struct.tests[i].time + ' - ' + self.archiveRun.struct.tests[i].name
                    temp_arr.append(temp)

                for i in range(len(temp_arr)):
                    self.ui.archive_time_comboBox.addItem(temp_arr[i])

                self.archive_time(0)
                self.ui.archive_time_comboBox.activated[int].connect(self.archive_time)

            if self.name_test == 'geo':
                temp_arr = []
                self.archiveGeo.select_file(date)
                self.date_select_archive_geo = self.archiveGeo.files_name_arr[self.archiveGeo.index_archive]

                for i in range(len(self.archiveGeo.struct.tests)):
                    temp = self.archiveGeo.struct.tests[i].time + ' - ' + self.archiveGeo.struct.tests[i].name
                    temp_arr.append(temp)

                for i in range(len(temp_arr)):
                    self.ui.archive_time_comboBox.addItem(temp_arr[i])

                self.archive_time(0)
                self.ui.archive_time_comboBox.activated[int].connect(self.archive_time)

        except Exception as e:
            self.logger.error(e)

    def archive_time(self, test):
        try:
            if self.name_test == 'run':
                date_arr_run = self.date_select_archive_run + ' - ' + self.archiveRun.struct.tests[test].time
                self.ui.archive_run_name_lineEdit.setText(self.archiveRun.struct.tests[test].name)
                self.ui.archive_run_serial_lineEdit.setText(self.archiveRun.struct.tests[test].serial)
                self.ui.archive_run_gear_lineEdit.setText(self.archiveRun.struct.tests[test].gear)
                self.ui.archive_run_direct_lineEdit.setText(self.archiveRun.struct.tests[test].direct)
                self.ui.archive_run_time_lineEdit.setText(self.archiveRun.struct.tests[test].duration_test)
                self.ui.archive_run_speed_lineEdit.setText(self.archiveRun.struct.tests[test].speed)
                self.ui.archive_run_date_lineEdit.setText(date_arr_run)
                self.ui.archive_run_oper_lineEdit.setText(self.archiveRun.struct.tests[test].user)
                self.ui.archive_run_temp1_lineEdit.setText(self.archiveRun.struct.tests[test].temp1)
                self.ui.archive_run_temp2_lineEdit.setText(self.archiveRun.struct.tests[test].temp2)
                self.ui.archive_run_temp3_lineEdit.setText(self.archiveRun.struct.tests[test].temp3)
                self.ui.archive_run_temp4_lineEdit.setText(self.archiveRun.struct.tests[test].temp4)
                self.ui.archive_run_temp5_lineEdit.setText(self.archiveRun.struct.tests[test].temp5)
                self.ui.archive_run_temp6_lineEdit.setText(self.archiveRun.struct.tests[test].temp6)
                self.ui.archive_run_temp7_lineEdit.setText(self.archiveRun.struct.tests[test].temp7)
                self.ui.archive_run_temp8_lineEdit.setText(self.archiveRun.struct.tests[test].temp8)

            if self.name_test == 'geo':
                self.ui.archive_angle_comboBox.clear()
                self.select_geo_test = test
                date_arr_geo = self.date_select_archive_geo + ' - ' + self.archiveGeo.struct.tests[test].time
                self.ui.archive_geometry_date_lineEdit.setText(date_arr_geo)
                self.ui.archive_geometry_name_lineEdit.setText(self.archiveGeo.struct.tests[test].name)
                self.ui.archive_geometry_operator_lineEdit.setText(self.archiveGeo.struct.tests[test].user)

                for i in range(len(self.archiveGeo.struct.tests[test].test_point)):
                    self.ui.archive_angle_comboBox.addItem(self.archiveGeo.struct.tests[test].test_point[i].angle)

                self.archive_geo_point(0)
                self.archive_geo_graph(0)
                self.ui.archive_angle_comboBox.activated[int].connect(self.archive_geo_point)
                self.ui.archive_angle_comboBox.activated[int].connect(self.archive_geo_graph)

        except Exception as e:
            self.logger.error(e)

    def archive_geo_point(self, point):
        try:
            test = self.select_geo_test
            interband_arr = []

            self.ui.archive_geometry_interband_lineEdit.setText(self.archiveGeo.struct.tests[test].test_point[point].interband)

            for i in range(len(self.archiveGeo.struct.tests[test].test_point)):
                interband_arr.append(int(self.archiveGeo.struct.tests[test].test_point[i].interband))

            self.delta_interband = max(interband_arr) - min(interband_arr)
            self.ui.archive_geometry_unparallel_lineEdit.setText(str(self.delta_interband))

        except Exception as e:
            self.logger.error(e)

    def archive_geo_graph(self, point):
        try:
            test = self.select_geo_test

            list_x_left = self.archiveGeo.struct.tests[test].test_point[point].line_left_X[:]
            list_y_left = self.archiveGeo.struct.tests[test].test_point[point].line_left_Y[:]
            list_x_right = self.archiveGeo.struct.tests[test].test_point[point].line_right_X[:]
            list_y_right = self.archiveGeo.struct.tests[test].test_point[point].line_right_Y[:]

            list_x_left = list_x_left[1::]
            list_y_left = list_y_left[1::]
            list_x_right = list_x_right[1::]
            list_y_right = list_y_right[1::]

            list_x_left = [float(x) for x in list_x_left]
            list_y_left = [float(x) for x in list_y_left]
            list_x_right = [float(x) for x in list_x_right]
            list_y_right = [float(x) for x in list_y_right]

            self.ui.archive_right_graph_widget.clear()
            self.ui.archive_right_graph_widget.showGrid(True, True)
            self.ui.archive_right_graph_widget.setBackground('w')

            self.ui.archive_left_graph_widget.clear()
            self.ui.archive_left_graph_widget.showGrid(True, True)
            self.ui.archive_left_graph_widget.setBackground('w')

            pen = pg.mkPen(color='k', width=3)

            self.ui.archive_left_graph_widget.plot(list_x_left, list_y_left, pen=pen)
            self.ui.archive_right_graph_widget.plot(list_x_right, list_y_right, pen=pen)

        except Exception as e:
            self.logger.error(e)

    def queryClose(self):
        try:
            self.signals.app_quit.emit()

        except Exception as e:
            self.logger.error(e)