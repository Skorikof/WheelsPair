from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTextEdit, QApplication, QLabel, QFrame
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont
from functools import partial
from Settings import DataWheelsRun, DataWheelsGeo
import LogPrg


class MySignals(QObject):
    finished = pyqtSignal(str, str)
    finished_serial_number = pyqtSignal(str)
    finished_wheelRun = pyqtSignal(object)
    finished_wheelGeo = pyqtSignal(object)
    cancel_edit = pyqtSignal()


style = '''
QPushButton {
         border: 1px solid #8f8f91;
         border-radius: 6px;
         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #f6f7fa, stop: 1 #dadbde);
     }

     QPushButton:pressed {
         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #dadbde, stop: 1 #f6f7fa);
     }

     QPushButton:default {
         border-color: navy; /* делаем кнопку по умолчанию выпуклой */
     }
     QPushButton:hover {
        background-color: #808080;
        color: #F0E68C;
     }
'''


class KeyS(QWidget):
    """description of class"""
    def __init__(self, win_g):
        super().__init__()
        try:
            self.resize(377,178)
            self.names_caps = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')',
                               'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ',
                               'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', '-',
                               'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', '.', ',', ':']
            self.names_small = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')',
                                'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ',
                                'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', '-',
                                'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.', ',', ':']

            self.names_caps_en = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')',
                                  'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}',
                                  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '-',
                                  'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ',', '#']

            self.names_small_en = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')',
                                   'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
                                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '-',
                                   'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '\'', ':']
            self.flag_caps = False

            self.mode_edit = 0

            self.type_keyb = ''

            self.layout = QGridLayout()
            self.label = QLabel()
            self.label.setFont(QFont('Arial', 16))

            self.label.setMinimumSize(QSize(410, 100))
            self.label.setMaximumSize(QSize(410, 100))

            self.label.setFrameShape(QFrame.Box)
            self.label.setFrameShadow(QFrame.Sunken)

            self.label.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            self.layout.addWidget(self.label, 0, 0, 1, 4)

            self.textEdit = QTextEdit()
            self.textEdit.setFont(QFont('Arial', 30))
            self.layout.addWidget(self.textEdit, 0, 4, 1, 9)

            self.name_lang = 'RU'

            self.new_name = ''
            self.new_rank = ''

            self.new_serial_number = ''

            self.newWheelRun = DataWheelsRun()
            self.newWheelGeo = DataWheelsGeo()

            self.signals = MySignals()
            self.buttons = {}
            for i in range(2, 6):
                for j in range(1, 13):
                    txt=self.names_small[12*(i-2)+j-1]
                    self.buttons[(i, j)] = QPushButton()
                    self.buttons[(i, j)].setObjectName = 'btn_'+ str(i) + '_' + str(j)
                    self.buttons[(i, j)].setText(txt)
                    self.buttons[(i, j)].setFixedHeight(100)
                    self.buttons[(i, j)].setFixedWidth(100)
                    self.buttons[(i, j)].setFont(QFont('Arial', 22, QFont.Bold))
                    self.layout.addWidget(self.buttons[(i, j)], i-1, j-1)
                    self.buttons[(i, j)].clicked.connect(partial(self.buttonClickedHandler, i, j))

            self.btn_caps=QPushButton('Caps')
            self.btn_caps.setObjectName = 'btn_caps'
            self.btn_caps.setFixedHeight(50)
            self.btn_caps.setFixedWidth(100)
            self.btn_caps.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_caps, 5, 0, 6, 1)
            self.btn_caps.clicked.connect(self.btnCapsHandler)

            self.btn_clear=QPushButton('Clear')
            self.btn_clear.setObjectName = 'btn_clear'
            self.btn_clear.setFixedHeight(50)
            self.btn_clear.setFixedWidth(200)
            self.btn_clear.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_clear, 5, 1, 6, 3)
            self.btn_clear.clicked.connect(self.btnClearHandler)

            self.btn_space=QPushButton('Space')
            self.btn_space.setObjectName = 'btn_space'
            self.btn_space.setFixedHeight(50)
            self.btn_space.setFixedWidth(400)
            self.btn_space.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_space, 5, 3, 6, 4)
            self.btn_space.clicked.connect(self.btnSpaceHandler)

            self.btn_enter=QPushButton('Enter')
            self.btn_enter.setObjectName = 'btn_space'
            self.btn_enter.setFixedHeight(50)
            self.btn_enter.setFixedWidth(200)
            self.btn_enter.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_enter, 5, 7, 6, 2)
            self.btn_enter.clicked.connect(self.btnEnterHandler)


            self.btn_sw_lang=QPushButton('EN')
            self.btn_sw_lang.setObjectName = 'btn_sw_lang'
            self.btn_sw_lang.setFixedHeight(50)
            self.btn_sw_lang.setFixedWidth(50)
            self.btn_sw_lang.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_sw_lang, 5, 9, 6, 2)
            self.btn_sw_lang.clicked.connect(self.btnSwitchLang)


            self.btn_cancel=QPushButton('Cancel')
            self.btn_cancel.setObjectName = 'btn_cancel'
            self.btn_cancel.setFixedHeight(50)
            self.btn_cancel.setFixedWidth(200)
            self.btn_cancel.setFont(QFont('Arial', 18))
            self.layout.addWidget(self.btn_cancel, 5, 10, 6, 2)
            self.btn_cancel.clicked.connect(self.btnCancelHandler)

            self.setLayout(self.layout)
            self.setStyleSheet(style)

            self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.CustomizeWindowHint) #|=False)
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)

            h = win_g.height()
            w = win_g.width()
            fg = self.frameGeometry()
            h1 = fg.height()
            w1 = fg.width()
            x = 1#(w-w1)/2 - w1
            y = (h-h1)/2 - h1/2-50

            self.move(x, y)

            self.InitKeys()
            self.setVisible(False)

            self.logger = LogPrg.get_logger(__name__)

        except Exception as e:
            self.logger.error(e)


    def InitKeys(self):
        try:
            self.label.setText('')
            self.textEdit.setText('')
            if self.type_keyb == 'serial':
                if self.mode_edit == 1:
                    self.label.setText('Введите серийный\nномер колёсной пары')

            if self.type_keyb == 'operators':
                if self.mode_edit == 1:
                    self.label.setText('Введите Ф.И.О')
                if self.mode_edit == 2:
                    self.label.setText('Введите должность')

            if self.type_keyb == 'wheels_run':
                if self.mode_edit == 1:
                    self.label.setText('Введите название\nколёсной пары:')
                if self.mode_edit == 2:
                    self.label.setText('Скорость вращения (м/с):')
                if self.mode_edit == 3:
                    self.label.setText('Максимальная\nтемпература (℃):')
                if self.mode_edit == 4:
                    self.label.setText('Время обкатки (мин):')

            if self.type_keyb == 'wheels_geo':
                if self.mode_edit == 1:
                    self.label.setText('Введите название\nколёсной пары:')
                if self.mode_edit == 2:
                    self.label.setText('Введите диаметр\nколеса (мм):')
                if self.mode_edit == 3:
                    self.label.setText('Максимальное\nбиение (мм):')
                if self.mode_edit == 4:
                    self.label.setText('Максимальная\nразница диаметров (мм):')
                if self.mode_edit == 5:
                    self.label.setText('Межбандажное\nрасстояние (мм):')
                if self.mode_edit == 6:
                    self.label.setText('Максимальная\nнепараллельность\nвнутренних ободов (мм):')
                if self.mode_edit == 7:
                    self.label.setText('Высота гребня (мм):')
                if self.mode_edit == 8:
                    self.label.setText('Толщина гребня (мм):')
                if self.mode_edit == 9:
                    self.label.setText('Максимальная разница\nв толщине гребней (мм):')
                if self.mode_edit == 10:
                    self.label.setText('Круг катания\nот торца (мм):')
                if self.mode_edit == 11:
                    self.label.setText('Ширина обода (мм):')
                if self.mode_edit == 12:
                    self.label.setText('Число соотношения\n1-го уклона')
                if self.mode_edit == 13:
                    self.label.setText('Число соотношения\n2-го уклона')

        except Exception as e:
            self.logger.error(e)

    def center(self):
        try:
            frameGm = self.frameGeometry()
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            centerPoint = QApplication.desktop().screenGeometry(screen).center()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())

        except Exception as e:
            self.logger.error(e)

    def btnSwitchLang(self):
        try:
            if self.name_lang == 'RU':
                self.name_lang = 'EN'
                self.btn_sw_lang.setText('RU')
                for i in range(2, 6):
                    for j in range(1, 13):
                        if self.flag_caps:
                            txt = self.names_caps_en[12*(i-2)+j-1]
                        else:
                            txt = self.names_small_en[12*(i-2)+j-1]
                        self.buttons[(i, j)].setText(txt)
            else:
                self.name_lang = 'RU'
                self.btn_sw_lang.setText('EN')
                for i in range(2, 6):
                    for j in range(1, 13):
                        if self.flag_caps:
                            txt = self.names_caps[12*(i-2)+j-1]
                        else:
                            txt = self.names_small[12*(i-2)+j-1]
                        self.buttons[(i, j)].setText(txt)

        except Exception as e:
            self.logger.error(e)

    def btnCancelHandler(self):
        try:
            if self.type_keyb == 'serial':
                pass
            else:
                self.signals.cancel_edit.emit()

        except Exception as e:
            self.logger.error(e)

    def btnEnterHandler(self):
        try:
            txt = self.textEdit.toPlainText()
            if len(txt) > 0:
                next_mode, flag_e = self.nextElemetns(txt)
                if flag_e:
                    if self.type_keyb == 'serial':
                        self.signals.finished_serial_number.emit(self.new_serial_number)
                    if self.type_keyb == 'operators':
                        self.signals.finished.emit(self.new_name, self.new_rank)
                    if self.type_keyb == 'wheels_run':
                        self.signals.finished_wheelRun.emit(self.newWheelRun)
                    if self.type_keyb == 'wheels_geo':
                        self.signals.finished_wheelGeo.emit(self.newWheelGeo)
                else:
                    self.mode_edit = next_mode
                    self.InitKeys()

        except Exception as e:
            self.logger.error(e)

    def btnClearHandler(self):
        try:
            txt = self.textEdit.toPlainText()
            txt = txt[:-1]
            self.textEdit.setText(txt)

        except Exception as e:
            self.logger.error(e)

    def btnSpaceHandler(self):
        try:
            txt_temp = self.textEdit.toPlainText() + ' '
            self.textEdit.setText(txt_temp)

        except Exception as e:
            self.logger.error(e)

    def btnCapsHandler(self):
        try:
            self.flag_caps = not self.flag_caps

            for i in range(2, 6):
                for j in range(1, 13):
                    if self.flag_caps:
                        self.btn_caps.setText('Small')
                        if self.name_lang == 'RU':
                            txt = self.names_caps[12 * (i - 2) + j - 1]
                        else:
                            txt = self.names_caps_en[12 * (i - 2) + j - 1]
                    else:
                        self.btn_caps.setText('Caps')
                        if self.name_lang == 'RU':
                            txt = self.names_small[12 * (i - 2) + j - 1]
                        else:
                            txt = self.names_small_en[12 * (i - 2) + j - 1]

                    self.buttons[(i, j)].setText(txt)

        except Exception as e:
            self.logger.error(e)

    def nextElemetns(self, txt_e):
        try:
            flag_finish = False
            next_mode = 0
            if self.type_keyb == 'serial':
                if self.mode_edit == 1:
                    self.new_serial_number = txt_e
                    next_mode = 2
                    flag_finish = True

            if self.type_keyb == 'operators':
                if self.mode_edit == 1:
                    self.new_name = txt_e
                    next_mode = 2
                if self.mode_edit == 2:
                    self.new_rank = txt_e
                    next_mode = 3
                    flag_finish = True

            if self.type_keyb == 'wheels_run':
                if self.mode_edit == 1:
                    self.newWheelRun.name = txt_e
                    next_mode = 2
                if self.mode_edit == 2:
                    if is_int(txt_e):
                        self.newWheelRun.speed = int(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 3:
                    if is_int(txt_e):
                        self.newWheelRun.max_temp = int(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 4:
                    if is_int(txt_e):
                        self.newWheelRun.time_test = int(txt_e)
                        next_mode = self.mode_edit+1
                        flag_finish = True
                    else:
                        next_mode = self.mode_edit

            if self.type_keyb == 'wheels_geo':
                if self.mode_edit == 1:
                    self.newWheelGeo.name = txt_e
                    next_mode = 2
                if self.mode_edit == 2:
                    if is_int(txt_e):
                        self.newWheelGeo.diameter = int(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 3:
                    if is_float(txt_e):
                        self.newWheelGeo.beat = float(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 4:
                    if is_float(txt_e):
                        self.newWheelGeo.diff_diameter = float(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 5:
                    if is_int(txt_e):
                        self.newWheelGeo.interband = int(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 6:
                    if is_float(txt_e):
                        self.newWheelGeo.unparallel = float(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 7:
                    if is_int(txt_e):
                        self.newWheelGeo.crest_high = int(txt_e)
                        next_mode = self.mode_edit+1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 8:
                    if is_int(txt_e):
                        self.newWheelGeo.crest_width = int(txt_e)
                        next_mode = self.mode_edit + 1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 9:
                    if is_float(txt_e):
                        self.newWheelGeo.crest_diff = float(txt_e)
                        next_mode = self.mode_edit + 1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 10:
                    if is_int(txt_e):
                        self.newWheelGeo.roll_circle = int(txt_e)
                        next_mode = self.mode_edit + 1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 11:
                    if is_int(txt_e):
                        self.newWheelGeo.width_rim = int(txt_e)
                        next_mode = self.mode_edit + 1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 12:
                    if is_int(txt_e):
                        self.newWheelGeo.one_slope = int(txt_e)
                        next_mode = self.mode_edit + 1
                    else:
                        next_mode = self.mode_edit

                if self.mode_edit == 13:
                    if is_int(txt_e):
                        self.newWheelGeo.two_slope = int(txt_e)
                        next_mode = self.mode_edit + 1
                        flag_finish = True

                    else:
                        next_mode = self.mode_edit

            return next_mode, flag_finish

        except Exception as e:
            self.logger.error(e)

    def buttonClickedHandler(self, i, j):
        try:
            txt_temp = self.textEdit.toPlainText() + self.buttons[(i, j)].text()
            self.textEdit.setText(txt_temp)
        except Exception as e:
            self.logger.error(e)

    def closeEvent(self, event):
        try:
            self.signals.finished.emit()

        except Exception as e:
            self.logger.error(e)


def moveToCenterScreen(win):
    try:
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        win_size = (win.frameSize().width(), win.frameSize().height())
        x = (screen_size[0] - win_size[0])#/2
        y = (screen_size[1] - win_size[1])#/2
        win.move(x, y)
    except Exception as e:
        print('{}'.format(e))


def is_float(txt):
    try:
        float(txt)
        return True
    except ValueError:
        return False


def is_int(txt):
    try:
        int(txt)
        return True
    except ValueError:
        return False
