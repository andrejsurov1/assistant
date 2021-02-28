# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets


class Model:
    def __init__(self):
        """в последующих функциях класса, 
        используется в качестве
        переподключения к БД"""
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self.c = self.conn.cursor()

    # функция выкидывающая окно ошибки
    @staticmethod
    def alert_warning():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('smth went wrong')
        msg.setWindowTitle("Error")
        msg.exec_()

    # функция добавлния записи в БД
    def addRecording(self, task_name, activate, task_description=None, hosts=None):
        self.__init__()
        try:
            # проверяет существование записи, с используемым именем
            exists = self.c.execute('''
                SELECT task_name FROM tasks WHERE task_name=?;
            ''', (task_name,)).fetchall()

            if not exists:
                pass
            else:
                self.c = self.conn.cursor()
                self.c.execute('''
                    DELETE FROM tasks WHERE task_name= ?;
                ''', (task_name,))

            # если пользователь захочет сделать задачу активной
            # сразу на этапе записи
            if int(activate) == 1:
                self.c = self.conn.cursor()
                try:
                    # снимает статус активации с других задач
                    self.c.execute('''
                        UPDATE tasks SET activate = -1 WHERE activate = 1;
                    ''')
                except IndexError:
                    pass

            # бросает исключение в случае отсутсвия
            # заданного имени задачи
            if str(task_name) == "":
                self.alert_warning()
            else:
                self.c = self.conn.cursor()
                self.c.execute('''
                        INSERT into tasks (task_name, task_description, activate, hosts) VALUES (?, ?, ?, ?);
                    ''', (str(task_name), str(task_description), int(activate), str(hosts))
                )
        except sqlite3.DatabaseError:
            pass
        self.conn.commit()
        self.conn.close()

    # функция получения всех записей из БД
    def take_data(self):
        self.__init__()
        tasks = self.c.execute('''
            SELECT * FROM tasks;
        ''').fetchall()
        self.conn.close()
        return tasks

    # получает конкретную запись из бд, по названию
    def take_recording(self, name_of_recording):
        self.__init__()
        task = self.c.execute('''
            SELECT * FROM tasks WHERE task_name = ?;
        ''', (name_of_recording,)).fetchall()
        self.conn.close()
        return task

    # функция удаления записи в БД
    def del_recording(self, task_name):
        self.__init__()
        self.c.execute('''
            DELETE FROM tasks WHERE task_name= ?;
        ''', (task_name,))
        self.conn.commit()
        self.conn.close()

    def take_active_task(self):
        self.__init__()
        return self.c.execute('''
            SELECT * FROM tasks WHERE activate = 1;
        ''').fetchall()
        self.conn.close()


obj = Model()
