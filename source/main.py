# -*- coding: utf-8 -*-

import sys
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QWidget

import gui
import block
from bd import *


class App(QtWidgets.QMainWindow, gui.Ui_MainWindow, object):
    def __init__(self):
        # опеределяем общий для элементов программы шрифт
        self.font = QtGui.QFont()
        self.font.setFamily("Bahnschrift SemiBold")
        self.font.setPointSize(9)

        # список выведенной информации, 
        # в блок подробного просмотра задачи
        self.list_of_view_data = []
        # список выведенных задач
        self.list_of_out_tasks = []

        # по умолчанию элемент "activate" неактивен
        self.activate = -1

        # задание базовых хар-ик окна программы
        # на основе полученного файла gui.py
        super().__init__()
        self.setupUi(self)
        super().setFixedSize(self.size())

        # "привязываем" функциональную часть,
        # к элементам интерфейса
        self.save_btn.clicked.connect(self.create_recording)
        self.checkBox.stateChanged.connect(self.check_activate)

    # функция отвечающая за статусность self.activate
    def check_activate(self, state):
        if state == Qt.Checked:
            self.activate = 1
        else:
            self.activate = -1

    # функция связывающая функцию создания записи
    # с входными данными
    def create_recording(self):
        # получаем данные для создания записи
        self.new_recording_label.setText(QtCore.QCoreApplication.translate("MainWindow", "добавление новой записи"))
        name_of_task = self.input_name.text()
        description_of_task = self.text_description.toPlainText()
        hosts = self.input_hosts.text()
        
        obj.addRecording(name_of_task, self.activate, description_of_task, hosts)
        
        # очищаем поля ввода
        self.input_hosts.clear()
            self.input_name.clear()
            self.text_description.clear()
            self.checkBox.setChecked(False)
            
            self.output_records()

    # функция редактирования записи
    def edit_rec(self, name_of_recording):
        # очищаем поля ввода
        self.input_hosts.clear()
        self.input_name.clear()
        self.text_description.clear()
        self.checkBox.setChecked(False)
        
        editing_task = obj.take_recording(name_of_recording)
        
        # заполняем полученные данные, в поля
        self.new_recording_label.setText(QtCore.QCoreApplication.translate("MainWindow", "редактирование записи"))
        self.input_name.insert(editing_task[0][0])
        self.input_hosts.insert(editing_task[0][3])
        if editing_task[0][2] == -1:
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)
        self.text_description.insertPlainText(editing_task[0][1])
        
        obj.del_recording(name_of_recording)

    # функция для вывода более подробной информации о задаче
    def view_recording(self, name_of_recording):
        if self.input_name.text() != "":
            self.create_recording()

        task = obj.take_recording(name_of_recording)

        # удаляем выведенные раннее элементы
        for item in self.list_of_view_data:
            for i in item:
                i.setParent(None)

        # очищаем список выведенных элементов
        self.list_of_view_data = []

        # данные о задаче
        info_of_record_label = QtWidgets.QLabel(f'''
            название задачи: {task[0][0]}
            статус задачи: {"выполняется" if task[0][2] == 1 else "неактивна"}
            блокируемые во время выполнения задачи сайты: {task[0][3]}
        '''.replace("   ", ""))
        info_of_record_label.setFont(self.font)

        # описание задачи
        description_label = QtWidgets.QLabel(f'описание задачи:\n{task[0][1]}\n')
        description_label.setFont(self.font)

        # размещаем созданные элементы
        self.viewlayout.addWidget(info_of_record_label)
        self.viewlayout.addWidget(description_label)
        
        self.list_of_view_data.append([
            info_of_record_label, description_label,
        ])

    # функция вывода записей из бд
    def output_records(self):
        # снимаем с отображения все записи, выведенные до этого
        for i in self.list_of_out_tasks:
            for item in i:
                item.setParent(None)

        # очищаем блок подробной информации о задаче
        for item in self.list_of_view_data:
            for i in item:
                i.setParent(None)

        # очищаем список выведенных задач
        self.list_of_out_tasks = []

        # получаем все существующие записи из БД
        tasks = obj.take_data()

        # итерируемся по списку задач
        for task in tasks:
            # блок предоставляющий краткую информацию о задаче 
            # (в боковом меню)
            task_label = QtWidgets.QLabel(
                f"""название: {task[0] if len(task[0]) < 10 else task[0][:11] + "..."}
               блокируемые сайты: {task[3] if len(task[3].split(",")) < 2 else task[3].split(",")[0] + "..."}
               состояние: {"выполняется" if task[2] == 1 else "неактивна"}
               описание: {task[1] if len(task[1]) < 8 else task[1][:9] + "..."}""".replace("   ", "")
            )
            task_label.setFont(self.font)

            # далее идет большой блок кода, отвечающий за кнопки 
            # взаимодействие с задачами
            # (подробнее, редактировать, удалить)
            del_button = QtWidgets.QPushButton(self.frame_3)
            del_button.setFont(self.font)
            del_button.setStyleSheet(
                "background-color: #f7e9ec;\n"
                "border: 2px solid #f66867;\n"
                "color: black;")
            del_button.setText(QCoreApplication.translate("MainWindow", "удалить"))
            # lambda checked используется по причине нужды, 
            # в передаче параметров функции(при вызове)
            del_button.clicked.connect(lambda checked, arg=task[0]: obj.del_recording(arg))
            del_button.clicked.connect(lambda event: self.output_records())

            edit_btn = QtWidgets.QPushButton(self.frame_3)
            edit_btn.setFont(self.font)
            edit_btn.setStyleSheet(
                "background-color: #f7e9ec;\n"
                "border: 2px solid #f66867;\n"
                "color: black;")
            edit_btn.setText(QtCore.QCoreApplication.translate("MainWindow", "редактировать"))
            # lambda checked используется по причине нужды, 
            # в передаче параметров функции(при вызове)
            edit_btn.clicked.connect(lambda checked, arg=task[0]: self.edit_rec(arg))

            view_btn = QtWidgets.QPushButton(self.centralwidget)
            view_btn.setGeometry(QtCore.QRect(290, 490, 221, 41))
            view_btn.setFont(self.font)
            view_btn.setStyleSheet(
                "background-color: #f7e9ec;\n"
                "border: 2px solid #f66867;\n"
                "color: black;")
            view_btn.setText(QCoreApplication.translate("MainWindow", "подробнее..."))
            # lambda checked используется по причине нужды, 
            # в передаче параметров функции(при вызове)
            view_btn.clicked.connect(lambda checked, arg=task[0]: self.view_recording(arg))
            
            # размещаем созданные элементы,
            # в боковой панели программы
            self.layout_tasks.addWidget(task_label)
            self.layout_tasks.addWidget(view_btn)
            self.layout_tasks.addWidget(edit_btn)
            self.layout_tasks.addWidget(del_button)

            self.list_of_out_tasks.append([task_label, del_button,
                                          edit_btn, view_btn])
        # выполняем блокировку сайтов, полученных 
        # от активной задачи
        block.main()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.output_records()
    window.show()
    try:
        app.exec_()
    finally:
        if window.input_name.text() != "":
            window.create_recording()
        block.main()
