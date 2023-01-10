import configparser
import LogPrg
from pathlib import Path
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


GL_VALUEDI = [0, 0, 0, 0, 0, 0, 0, 0]


class PrgProperties(object):
    def __init__(self):
        self.state = -1
        self.mode = ''
        self.operator = ''
        self.rank = ''
        self.set_operator = False
        self.questionMode = 0
        self.is_question = False
        self.query_serial = False
        self.test_run = False
        self.count_testGeo = 2
        self.test_geo = False
        self.type_wheel = ''
        self.direct_run = ''
        self.type_gear = ''
        self.type_carrier = ''
        self.serial_num_run = 0
        self.serial_num_geo = 0
        self.date_start_run = ''
        self.date_start_geo = ''


class StructWheels(object):
    def __init__(self):
        self.wheelsRun = []
        self.wheelsGeo = []


class DataWheelsRun(object):
    def __init__(self):
        self.name = ''
        self.speed = 0
        self.max_temp = 0
        self.time_test = 0


class DataWheelsGeo(object):
    def __init__(self):
        self.name = ''
        self.diameter = 0
        self.beat = 0
        self.diff_diameter = 0
        self.interband = 0
        self.unparallel = 0
        self.crest_high = 0
        self.crest_width = 0
        self.crest_diff = 0
        self.roll_circle = 0
        self.width_rim = 0
        self.one_slope = 0
        self.two_slope = 0


class PortSettings(object):
    def __init__(self):
        self.logger = LogPrg.get_logger(__name__)
        try:
            config = configparser.ConfigParser()
            config.read("Settings.ini")
            self.name = 'COM' + config.get('ComPort', 'NumberPort')
            str_p = config.get('ComPort', 'PortSettings')
            dim_t = str_p.split(',')
            self.baudrate = int(dim_t[0])
            self.parity = dim_t[1]
            self.databits = dim_t[2]
            self.stopbits = int(dim_t[3])
            self.client = ModbusClient()

            a = self.initPort()

        except Exception as e:
            self.logger.error(e)

    def initPort(self):
        try:
            self.client = ModbusClient(metod='rtu', port=self.name,
                                       parity=self.parity,
                                       baudrate=self.baudrate,
                                       databits=self.databits,
                                       stopbits=self.stopbits,
                                       strict=False)

            self.port_connect = self.client.connect()

            if self.port_connect:
                return True
            else:
                return False

        except Exception as e:
            self.logger.error(e)


class Devices(object):
    def __init__(self):
        self.devices = []


class Registers(object):
    def __init__(self):
        self.dev_id = 0
        self.dev_name = ''
        self.registers = []


class SettingsRegisters(object):
    def __init__(self):
        self.bytes = 0
        self.name_r = ''
        self.address_r = 0
        self.type_r = 'R'
        self.tag = ''
        self.dev_node = ''
        self.type_IO = ''


class SettingsDev(object):
    def __init__(self):
        self.logger = LogPrg.get_logger(__name__)
        self.struct = Devices()
        self.fillStruct()

    def fillStruct(self):
        count_dev = -1
        try:
            path = Path('Settings.ini')
            if not path.exists():
                txt_log = 'File "Settings.ini" is not found!'
                self.logger.error(txt_log)

            self.config = configparser.ConfigParser()
            self.config.read('Settings.ini')
            for i in range(len(self.config.sections())):
                try:
                    temp_val = self.config["Device" + str(i)]["SlaveID"]
                    if len(temp_val) > 0:
                        count_dev += 1
                        self.struct.devices.append(Registers())
                        self.struct.devices[count_dev].dev_id = temp_val
                        temp_val = self.config["Device" + str(i)]["Name"]
                        self.struct.devices[count_dev].dev_name = temp_val
                        temp_val = self.config["Device" + str(i)]["Node"]
                        node = temp_val
                        temp_val = self.config["Device" + str(i)]["Type"]
                        type_io = temp_val

                        count_regs = -1
                        for j in range(100):
                            try:
                                temp_val = self.config["Device" + str(i)]["Reg" + str(j)]
                                count_regs += 1
                                self.struct.devices[count_dev].registers.append(SettingsRegisters())
                                self.struct.devices[count_dev].registers[count_regs].dev_node = node
                                self.struct.devices[count_dev].registers[count_regs].type_IO = type_io
                                temp_m = str.split(temp_val, ",")
                                self.struct.devices[count_dev].registers[count_regs].bytes = temp_m[0]
                                self.struct.devices[count_dev].registers[count_regs].address_r = temp_m[1]
                                self.struct.devices[count_dev].registers[count_regs].name_r = temp_m[2]
                                self.struct.devices[count_dev].registers[count_regs].type_r = temp_m[3]
                                self.struct.devices[count_dev].registers[count_regs].tag = temp_m[4]

                            except:
                                pass

                except:
                    pass

        except Exception as e:
            print(e)

    def getParam(self, section, key):
        nam_p = ''
        try:
            nam_p = self.config.get(section, key)
            return nam_p

        except Exception as e:
            print(e) 
            return nam_p

    def getValue(self, mode, section, key):
        try:
            val = ''
            if mode == 'reg':
                ind = 1
            if mode == 'tag':
                ind = 4
            str_t = self.config.get(section, key)
            temp_m = str.split(str_t, ",")
            val = temp_m[ind]
            return val

        except Exception as e:
            print(e)
            return val


class RegisterStruct(object):
    def __init__(self):
        self.node = ''
        self.tag = ''
        self.num_bit = 0
        self.value_bit = -1


class DIGeo(object):
    def __init__(self):
        self.sensor_distance_plank_1 = RegisterStruct()
        self.sensor_distance_plank_2 = RegisterStruct()
        self.sensor_distance_plank_3 = RegisterStruct()
        self.sensor_moving_cone = RegisterStruct()
        self.sensor_platform_down_position = RegisterStruct()
        self.clamp_pair = RegisterStruct()
        self.unclamp_pair = RegisterStruct()
        self.sensor_contact_pair_prism = RegisterStruct()
        self.carrier_left_start_position = RegisterStruct()
        self.carrier_right_start_position = RegisterStruct()
        self.sensor_initial_state_bandage = RegisterStruct()
        self.sensor_initial_state_left_cone = RegisterStruct()
        self.sensor_initial_state_right_cone = RegisterStruct()
        self.sensor_unlock_left_cone = RegisterStruct()
        self.sensor_unlock_right_cone = RegisterStruct()


class DOGeo(object):
    def __init__(self):
        self.clamp_centres = RegisterStruct()
        self.clamp_wedges = RegisterStruct()
        self.move_laser_position_1 = RegisterStruct()
        self.move_laser_position_2 = RegisterStruct()
        self.move_bandage_distance = RegisterStruct()
        self.move_sensor_profile_left_wheel = RegisterStruct()
        self.move_sensor_profile_right_wheel = RegisterStruct()
        self.block_sensor_wheel_move_platform_up = RegisterStruct()
        self.activate_platform = RegisterStruct()
        self.clamp_engine = RegisterStruct()


class DIRun(object):
    def __init__(self):
        self.sensor_fence_cardan_gear_1 = RegisterStruct()
        self.sensor_connect_cardan_gear_1 = RegisterStruct()
        self.sensor_fence_cardan_gear_2 = RegisterStruct()
        self.sensor_connect_cardan_gear_2 = RegisterStruct()
        self.sensor_position_carriage_1 = RegisterStruct()
        self.sensor_position_carriage_2 = RegisterStruct()
        self.sensor_position_carriage_3 = RegisterStruct()
        self.sensor_count_turnover_wheels = RegisterStruct()
        self.relay_pressure = RegisterStruct()
        self.sensor_fixation_mobile_carriage = RegisterStruct()
        self.button_stop_test = RegisterStruct()


class DORun(object):
    def __init__(self):
        self.connect_engine_gear_1 = RegisterStruct()
        self.connect_engine_gear_2 = RegisterStruct()
        self.clamp_brake = RegisterStruct()
        self.clamp_engine_roller = RegisterStruct()
        self.carriage_latch_pinch = RegisterStruct()
        self.carriage_latch_letsGo = RegisterStruct()


class AIRun(object):
    def __init__(self):
        self.sensor_temp = RegisterStruct()


class PrgSignals(object):
    def __init__(self):
        self.DIRun = DIRun()
        self.DORun = DORun()
        self.AIRun = AIRun()
        self.DIGeo = DIGeo()
        self.DOGeo = DOGeo()
