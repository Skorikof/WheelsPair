import configparser
import LogPrg
from pathlib import Path


class Operators(object):
    def __init__(self):
        self.names = []
        self.ranks = []
        self.config = configparser.ConfigParser()
        self.current_index = -1

        self.logger = LogPrg.get_logger(__name__)

        path = Path('Operators.ini')
        if not path.exists():
            path.touch()
            self.logger.info('File "Operators.ini" is create')

    def updateOperatorsList(self):
        try:
            self.names = []
            self.ranks = []
            self.config.read("Operators.ini")
            for section in self.config.sections():
                try:
                    for key in self.config[section]:
                        temp_val = self.config.get(section, key)
                        if key == 'name':
                            self.names.append(temp_val)
                        if key == 'rank':
                            self.ranks.append(temp_val)

                except Exception as e:
                    self.logger.error(e)

        except Exception as e:
            self.logger.error(e)

    def deleteOperator(self, index_del):
        try:
            if self.current_index >= 0:
                txt_log = 'OPERATOR ' + self.ranks[index_del] + ' ' + self.names[index_del] + ' is DELETE'
                self.logger.info(txt_log)

                self.names.pop(index_del)
                self.ranks.pop(index_del)

                self.config.clear()

                for i in range(len(self.names)):
                    nam_section = 'Operator' + str(i)
                    self.config.add_section(nam_section)
                    self.config.set(nam_section, 'name', self.names[i])
                    self.config.set(nam_section, 'rank', self.ranks[i])

                with open('Operators.ini', "w") as configfile:
                    self.config.write(configfile)
            else:
                pass

        except Exception as e:
            self.logger.error(e)

    def addNewOperator(self, name, rank):
        try:
            max_rec = len(self.config.sections())
            name_section = 'Operator' + str(max_rec)
            self.config.add_section(name_section)
            self.config.set(name_section, 'name', name)
            self.config.set(name_section, 'rank', rank)

            with open('Operators.ini', "w") as configfile:
                self.config.write(configfile)

            txt_log = 'OPERATOR ' + rank + ' ' + name + ' is ADDED'
            self.logger.info(txt_log)

        except Exception as e:
            self.logger.error(e)