from pathlib import Path
from datetime import datetime


class FileArchive(object):
    def __init__(self):
        self.tests = []


class TestArchive(object):
    def __init__(self):
        self.run_test_id = 0
        self.time = ''
        self.user = ''
        self.serial = ''
        self.name = ''
        self.gear = ''
        self.direct = ''
        self.duration_test = ''
        self.speed = ''
        self.temp1 = ''
        self.temp2 = ''
        self.temp3 = ''
        self.temp4 = ''
        self.temp5 = ''
        self.temp6 = ''
        self.temp7 = ''
        self.temp8 = ''


class RunArchive(object):
    def __init__(self):
        try:
            self.init_arch()

        except Exception as e:
            print('{}'.format(e))

    def init_arch(self):
        try:
            source_dir = Path('archiveRun/')
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
            print('{}'.format(e))


    def select_file(self, data):
        """принимает номер файла в папке архива"""
        try:
            self.struct = FileArchive()
            self.count_tests = -1

            self.index_archive = self.files_name_arr.index(data)

            with open(self.files_arr[self.index_archive]) as f:
                self.glob_arr = f.readlines()
                for i in range(len(self.glob_arr)):

                    if self.glob_arr[i].find('Испытание') >= 0:
                        self.count_tests += 1
                        self.struct.tests.append(TestArchive())
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].run_test_id = temp_val[1][:-1]

                    if self.glob_arr[i].find('Время') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].time = temp_val[1][:-1]

                    if self.glob_arr[i].find('Оператор') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].user = temp_val[1][:-1]

                    if self.glob_arr[i].find('Серийный номер') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].serial = temp_val[1][:-1]

                    if self.glob_arr[i].find('Наименование') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].name = temp_val[1][:-1]

                    if self.glob_arr[i].find('Тип привода') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].gear = temp_val[1][:-1]

                    if self.glob_arr[i].find('Направление') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].direct = temp_val[1][:-1]

                    if self.glob_arr[i].find('Продолжительность') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].duration_test = temp_val[1][:-1]

                    if self.glob_arr[i].find('Скорость') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].speed = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 1') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp1 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 2') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp2 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 3') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp3 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 4') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp4 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 5') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp5 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 6') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp6 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 7') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp7 = temp_val[1][:-1]

                    if self.glob_arr[i].find('Температура 8') >= 0:
                        temp_val = self.glob_arr[i].split(';')
                        self.struct.tests[self.count_tests].temp8 = temp_val[1][:-1]

        except Exception as e:
            print('{}'.format(e))