import configparser
import LogPrg
from Settings import StructWheels, DataWheelsRun, DataWheelsGeo


class Wheels(object):
    def __init__(self, prg):
        self.struct = StructWheels()
        self.config = configparser.ConfigParser()
        self.current_index_run = 0
        self.current_index_geo = 0
        self.prg = prg

        self.logger = LogPrg.get_logger(__name__)

    def updateWheelsList(self):
        try:
            if self.prg.type_wheel == 'run':
                self.config.clear()
                self.struct.wheelsRun.clear()
                self.config.read('WheelsRun.ini')
                index_r = -1
                for section in self.config.sections():
                    try:
                        index_r += 1
                        self.struct.wheelsRun.append(DataWheelsRun())
                        for key in self.config[section]:
                            temp_val = self.config.get(section, key)
                            if key == 'name':
                                self.struct.wheelsRun[index_r].name = temp_val
                            if key == 'speed':
                                self.struct.wheelsRun[index_r].speed = int(temp_val)
                            if key == 'max_temp':
                                self.struct.wheelsRun[index_r].max_temp = int(temp_val)
                            if key == 'time_test':
                                self.struct.wheelsRun[index_r].time_test = int(temp_val)

                    except Exception as e:
                        self.logger.error(e)

            if self.prg.type_wheel == 'geo':
                self.config.clear()
                self.struct.wheelsGeo.clear()
                self.config.read('WheelsGeo.ini')
                index_g = -1
                for section in self.config.sections():
                    try:
                        index_g += 1
                        self.struct.wheelsGeo.append(DataWheelsGeo())
                        for key in self.config[section]:
                            temp_val = self.config.get(section,key)
                            if key == 'name':
                                self.struct.wheelsGeo[index_g].name = temp_val
                            if key == 'diameter':
                                self.struct.wheelsGeo[index_g].diameter = float(temp_val)
                            if key == 'beat':
                                self.struct.wheelsGeo[index_g].beat = float(temp_val)
                            if key == 'diff_diameter':
                                self.struct.wheelsGeo[index_g].diff_diameter = float(temp_val)
                            if key == 'interband':
                                self.struct.wheelsGeo[index_g].interband = float(temp_val)
                            if key == 'unparallel':
                                self.struct.wheelsGeo[index_g].unparallel = float(temp_val)
                            if key == 'crest_high':
                                self.struct.wheelsGeo[index_g].crest_high = float(temp_val)
                            if key == 'crest_width':
                                self.struct.wheelsGeo[index_g].crest_width = float(temp_val)
                            if key == 'crest_diff':
                                self.struct.wheelsGeo[index_g].crest_diff = float(temp_val)
                            if key == 'roll_circle':
                                self.struct.wheelsGeo[index_g].roll_circle = float(temp_val)
                            if key == 'width_rim':
                                self.struct.wheelsGeo[index_g].width_rim = float(temp_val)
                            if key == 'one_slope':
                                self.struct.wheelsGeo[index_g].one_slope = float(temp_val)
                            if key == 'two_slope':
                                self.struct.wheelsGeo[index_g].two_slope = float(temp_val)

                    except Exception as e:
                        self.logger.error(e)

        except Exception as e:
            self.logger.error(e)

    def deleteWheels(self, index_del):
        try:
            if self.prg.type_wheel == 'run':
                txt_log = 'name = {}, speed = {}, max_temp = {}, time_test = {}'.format(
                            self.struct.wheelsRun[index_del].name,
                            self.struct.wheelsRun[index_del].speed,
                            self.struct.wheelsRun[index_del].max_temp,
                            self.struct.wheelsRun[index_del].time_test)

                self.logger.info('WheelsPair from RUN is DELETED: ' + txt_log)

                self.struct.wheelsRun.pop(index_del)
                self.config.clear()
                for i in range(len(self.struct.wheelsRun)):
                    nam_section = 'Wheels' + str(i)
                    self.config.add_section(nam_section)

                    self.config.set(nam_section, 'name', str(self.struct.wheelsRun[i].name))
                    self.config.set(nam_section, 'speed', str(self.struct.wheelsRun[i].speed))
                    self.config.set(nam_section, 'max_temp', str(self.struct.wheelsRun[i].max_temp))
                    self.config.set(nam_section, 'time_test', str(self.struct.wheelsRun[i].time_test))

                with open('WheelsRun.ini', "w") as configfile:
                    self.config.write(configfile)

            if self.prg.type_wheel == 'geo':
                txt_log = 'name = {}, diameter = {}, beat = {}, diff_diameter = {}, interband = {}, unparallel = {},' \
                          'crest_high = {}, crest_width = {}, crest_diff = {}, roll_circle = {}, width_rim = {},' \
                          'one_slope = {}, two_slope = {}'.format(
                            self.struct.wheelsGeo[index_del].name,
                            self.struct.wheelsGeo[index_del].diameter,
                            self.struct.wheelsGeo[index_del].beat,
                            self.struct.wheelsGeo[index_del].diff_diameter,
                            self.struct.wheelsGeo[index_del].interband,
                            self.struct.wheelsGeo[index_del].unparallel,
                            self.struct.wheelsGeo[index_del].crest_high,
                            self.struct.wheelsGeo[index_del].crest_width,
                            self.struct.wheelsGeo[index_del].crest_diff,
                            self.struct.wheelsGeo[index_del].roll_circle,
                            self.struct.wheelsGeo[index_del].width_rim,
                            self.struct.wheelsGeo[index_del].one_slope,
                            self.struct.wheelsGeo[index_del].two_slope)

                self.logger.info('WheelsPair from GEO is DELETED: ' + txt_log)

                self.struct.wheelsGeo.pop(index_del)
                self.config.clear()
                for i in range(len(self.struct.wheelsGeo)):
                    nam_section = 'Wheels' + str(i)
                    self.config.add_section(nam_section)

                    self.config.set(nam_section, 'name', str(self.struct.wheelsGeo[i].name))
                    self.config.set(nam_section, 'diameter', str(self.struct.wheelsGeo[i].diameter))
                    self.config.set(nam_section, 'beat', str(self.struct.wheelsGeo[i].beat))
                    self.config.set(nam_section, 'diff_diameter', str(self.struct.wheelsGeo[i].diff_diameter))
                    self.config.set(nam_section, 'interband', str(self.struct.wheelsGeo[i].interband))
                    self.config.set(nam_section, 'unparallel', str(self.struct.wheelsGeo[i].unparallel))
                    self.config.set(nam_section, 'crest_high', str(self.struct.wheelsGeo[i].crest_high))
                    self.config.set(nam_section, 'crest_width', str(self.struct.wheelsGeo[i].crest_width))
                    self.config.set(nam_section, 'crest_diff', str(self.struct.wheelsGeo[i].crest_diff))
                    self.config.set(nam_section, 'roll_circle', str(self.struct.wheelsGeo[i].roll_circle))
                    self.config.set(nam_section, 'width_rim', str(self.struct.wheelsGeo[i].width_rim))
                    self.config.set(nam_section, 'one_slope', str(self.struct.wheelsGeo[i].one_slope))
                    self.config.set(nam_section, 'two_slope', str(self.struct.wheelsGeo[i].two_slope))

                with open('WheelsGeo.ini', "w") as configfile:
                    self.config.write(configfile)

        except Exception as e:
            self.logger.error(e)

    def addNewWheels(self, obj):
        try:
            if self.prg.type_wheel == 'run':
                max_rec = len(self.struct.wheelsRun)
                nam_section = 'Wheels' + str(max_rec)
                self.config.add_section(nam_section)
                self.config.set(nam_section, 'name', str(obj.name))
                self.config.set(nam_section, 'speed', str(obj.speed))
                self.config.set(nam_section, 'max_temp', str(obj.max_temp))
                self.config.set(nam_section, 'time_test', str(obj.time_test))

                with open('WheelsRun.ini', 'w') as configfile:
                    self.config.write(configfile)

                txt_log = 'name = {}, speed = {}, max_temp = {}, time_test = {}'.format(obj.name, obj.speed,
                                                                                        obj.max_temp, obj.time_test)

                self.logger.info('WheelsPair in RUN is ADDED: ' + txt_log)

            if self.prg.type_wheel == 'geo':
                max_rec = len(self.struct.wheelsGeo)
                nam_section = 'Wheels' + str(max_rec)
                self.config.add_section(nam_section)
                self.config.set(nam_section, 'name', str(obj.name))
                self.config.set(nam_section, 'diameter', str(obj.diameter))
                self.config.set(nam_section, 'beat', str(obj.beat))
                self.config.set(nam_section, 'diff_diameter', str(obj.diff_diameter))
                self.config.set(nam_section, 'interband', str(obj.interband))
                self.config.set(nam_section, 'unparallel', str(obj.unparallel))
                self.config.set(nam_section, 'crest_high', str(obj.crest_high))
                self.config.set(nam_section, 'crest_width', str(obj.crest_width))
                self.config.set(nam_section, 'crest_diff', str(obj.crest_diff))
                self.config.set(nam_section, 'roll_circle', str(obj.roll_circle))
                self.config.set(nam_section, 'width_rim', str(obj.width_rim))
                self.config.set(nam_section, 'one_slope', str(obj.one_slope))
                self.config.set(nam_section, 'two_slope', str(obj.two_slope))

                with open('WheelsGeo.ini', 'w') as configfile:
                    self.config.write(configfile)

                txt_log = 'name = {}, diameter = {}, beat = {}, diff_diameter = {}, interband = {}, unparallel = {},' \
                          'crest_high = {}, crest_width = {}, crest_diff = {}, roll_circle = {}, width_rim = {},' \
                          'one_slope = {}, two_slope = {}'.format(obj.name, obj.diameter, obj.beat, obj.diff_diameter,
                                                                  obj.interband, obj.unparallel, obj.crest_high,
                                                                  obj.crest_width, obj.crest_diff, obj.roll_circle,
                                                                  obj.width_rim, obj.one_slope, obj.two_slope)

                self.logger.info('WheelsPair in GEO is ADDED: ' + txt_log)

        except Exception as e:
            self.logger.error(e)

