import sys
from PyQt5 import QtWidgets, QtCore
import main_window
import mko_unit
import configparser
import os


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        #
        self.config = None
        self.config_file = None
        # контейнеры для вставки юнитов
        self.units_widgets = mko_unit.Widgets(self.scrollAreaWidgetContents)
        self.units_widgets.action.connect(self.data_table_slot)
        self.setLayout(self.units_widgets)
        # привязка сигналов к кнопкам
        self.AddUnitPButt.clicked.connect(self.units_widgets.add_unit)
        self.DltUnitPButt.clicked.connect(self.dlt_unit)
        self.DltAllUnitsPButt.clicked.connect(self.units_widgets.delete_all_units)
        self.LoadCfgPButt.clicked.connect(self.load_cfg)
        self.SaveCfgPButt.clicked.connect(self.save_cfg)
        #
        self.load_init_cfg()

    def dlt_unit(self):
        n = self.DltUnitNumSBox.value()
        self.units_widgets.delete_unit_by_num(n)
        pass

    def data_table_slot(self):
        # на всякий пожарный сохраняем текущую конфигурацию
        self.save_init_cfg()
        #
        table_data = self.units_widgets.table_data
        self.DataTable.setRowCount(len(table_data))
        for row in range(len(table_data)):
            for column in range(self.DataTable.columnCount()):
                try:
                    table_item = QtWidgets.QTableWidgetItem(table_data[row][column])
                    self.DataTable.setItem(row, column, table_item)
                except IndexError:
                    pass
        pass

    def load_init_cfg(self):
        self.config = configparser.ConfigParser()
        file_name = "init.cfg"
        self.config.read(file_name)
        # print(self.config.sections())
        if self.config.sections():
            self.units_widgets.load_cfg(self.config)
        else:
            self.units_widgets.add_unit()
        pass

    def save_init_cfg(self):
        self.config = configparser.ConfigParser()
        self.config = self.units_widgets.get_cfg(self.config)
        # print(self.config)
        file_name = "init.cfg"
        try:
            with open(file_name, 'w') as configfile:
                self.config.write(configfile)
        except FileNotFoundError:
            pass
        pass

    def load_cfg(self):
        config = configparser.ConfigParser()
        home_dir = os.getcwd()
        try:
            os.mkdir(home_dir + "\\Config")
        except OSError:
            pass
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Открыть файл конфигурации",
            home_dir + "\\Config",
            r"config(*.cfg);;All Files(*)"
        )[0]
        config.read(file_name)
        self.units_widgets.load_cfg(config)
        pass

    def save_cfg(self):
        home_dir = os.getcwd()
        config = configparser.ConfigParser()
        config = self.units_widgets.get_cfg(self.config)
        try:
            os.mkdir(home_dir + "\\Config")
        except OSError:
            pass
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Сохранить файл конфигурации",
            home_dir + "\\Config",
            r"config(*.cfg);;All Files(*)"
        )[0]
        try:
            with open(file_name, 'w') as configfile:
                config.write(configfile)
        except FileNotFoundError:
            pass
        pass

    def closeEvent(self, event):
        self.save_init_cfg()
        self.close()
        pass

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
