from pathlib import Path
from datetime import datetime
import LogPrg


class FileArchive(object):
    def __init__(self):
        self.tests = []


class TestArchive(object):
    def __init__(self):
        self.geo_test_id = 0
        self.time = ''
        self.user = ''
        self.name = ''
        self.serial = ''
        self.test_point = []


class PointArchive(object):
    def __init__(self):
        self.angle = 0
        self.interband = 0
        self.line_left_X = []
        self.line_left_Y = []
        self.line_right_X = []
        self.line_right_Y = []


class GeoArchive(object):
    def __init__(self):
        try:
            self.logger = LogPrg.get_logger(__name__)
            self.init_arch()

        except Exception as e:
            self.logger.error(e)

    def init_arch(self):
        try:
            source_dir = Path('archiveGeo/')
            self.files_dir = source_dir.glob('*.csv')

            self.files_arr = []
            self.files_name_arr = []
            self.files_name_sort = []
            self.count_files = 0

            for i in self.files_dir:
                self.count_files += 1
                self.files_arr.append(i)
                self.files_name_arr.append(i.stem)
                self.files_name_sort.append(i.stem)

                """сортировка списка файлов по дате"""
                self.files_name_sort.sort(key=lambda date: datetime.strptime(date, "%d.%m.%Y"), reverse=True)

        except Exception as e:
            self.logger.error(e)

    def select_file(self, data):
        """принимает номер файла в папке архива"""
        try:
            self.struct = FileArchive()
            self.count_tests = -1
            self.count_point = -1

            self.index_archive = self.files_name_arr.index(data)

            with open(self.files_arr[self.index_archive]) as f:
                self.glob_arr = f.readlines()

                flag_graph_left = True
                flag_graph_right = True

                for i in range(len(self.glob_arr)):
                    if self.glob_arr[i].find('Испытание') >= 0:
                        self.count_tests += 1
                        flag_graph_left = False
                        flag_graph_right = False
                        self.struct.tests.append(TestArchive())
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].geo_test_id = temp_val[1][:-1]

                    if self.glob_arr[i].find('Время') >= 0:
                        flag_graph_left = False
                        flag_graph_right = False
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].time = temp_val[1][:-1]

                    if self.glob_arr[i].find('Оператор') >= 0:
                        flag_graph_left = False
                        flag_graph_right = False
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].user = temp_val[1][:-1]

                    if self.glob_arr[i].find('Наименование') >= 0:
                        flag_graph_left = False
                        flag_graph_right = False
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].name = temp_val[1][:-1]

                    if self.glob_arr[i].find('Серийный номер') >= 0:
                        flag_graph_left = False
                        flag_graph_right = False
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].serial = temp_val[1][:-1]

                    if self.glob_arr[i].find('Точка') >= 0:
                        self.count_point += 1
                        flag_graph_left = False
                        flag_graph_right = False
                        self.struct.tests[self.count_tests].test_point.append(PointArchive())


                    if self.glob_arr[i].find('Угол') >= 0:
                        flag_graph_left = False
                        flag_graph_right = False
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].test_point[self.count_point].angle = temp_val[1][:-1]

                    if self.glob_arr[i].find('Межбандажное') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].test_point[self.count_point].interband = temp_val[1][:-1]

                    if self.glob_arr[i].find('Левое') >= 0:
                        flag_graph_left = True
                        flag_graph_right = False

                    if self.glob_arr[i].find('Правое') >= 0:
                        flag_graph_right = True
                        flag_graph_left = False

                    if flag_graph_left:
                        temp_val = self.glob_arr[i].split(';')
                        temp_val[0] = temp_val[0].replace(',', '.')
                        temp_val[1] = temp_val[1].replace(',', '.')
                        self.struct.tests[self.count_tests].test_point[self.count_point].line_left_X.append(temp_val[0])
                        self.struct.tests[self.count_tests].test_point[self.count_point].line_left_Y.append(temp_val[1][:-1])

                    if flag_graph_right:
                        temp_val = self.glob_arr[i].split(';')
                        temp_val[0] = temp_val[0].replace(',', '.')
                        temp_val[1] = temp_val[1].replace(',', '.')
                        self.struct.tests[self.count_tests].test_point[self.count_point].line_right_X.append(temp_val[0])
                        self.struct.tests[self.count_tests].test_point[self.count_point].line_right_Y.append(temp_val[1][:-1])

        except Exception as e:
            self.logger.error(e)
