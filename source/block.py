# -*- coding: utf-8 -*-

import sys
from bd import obj
from PyQt5 import QtWidgets


host_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
redirect = "127.0.0.1"
info = '#added by the program "assistant"'


def alert_warning():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText('To use, you must run the program as administrator!')
    msg.setWindowTitle("PermissionError:")
    msg.exec_()


# функция очищающая внесенные изменения
def remove_changes():
    try:
        with open(host_path, "r+") as file:
            content = file.readlines()
            # переходим в начало файла
            file.seek(0)
            for line in content:
                if not info in line:
                    file.write(line)
                # стираем содержимое файла 
                # до текущей позиции
                file.truncate()
    except PermissionError:
        alert_warning()
        sys.exit()


# функция, которая блокирует список доменных имен
def block_hosts(website_list):
    try:
        remove_changes()

        with open(host_path, "r+") as file:
            data = file.read()
            for website in website_list:
                if website in data: 
                    pass
                else:
                    file.write(f'{redirect} {website} {info}\n')
    except PermissionError:
        alert_warning()
        sys.exit()


def main():
    try:
        hosts_to_block = obj.take_active_task()[0][3].split(",")
        block_hosts(hosts_to_block)
    except IndexError:
        remove_changes()
