from PyQt5.QtWidgets import QMessageBox
from qgis._core import Qgis


def simple_message(iface, msg, level=Qgis.Info):
    widget = iface.messageBar().createMessage(msg)
    iface.messageBar().pushWidget(widget, level, 5)


def basic_message(iface, msg1, msg2, level=Qgis.Info):
    widget = iface.messageBar().createMessage(msg1, msg2)
    iface.messageBar().pushWidget(widget, level, 5)


def stacked_message(iface, msg1, dict_class_name, level=Qgis.Warning):
    msg2 = ""
    for className in dict_class_name:
        msg2 = msg2 + "\n" + className + " ("
        for ref in dict_class_name[className]:
            msg2 = msg2 + ref + ", "
        msg2 = msg2[:-2]
        msg2 = msg2 + ")"
    widget = iface.messageBar().createMessage(msg1, msg2)
    iface.messageBar().pushWidget(widget, level, 5)


def confirmation_message(iface, msg):
    reply = QMessageBox.question(iface.mainWindow(), 'Continuez?', msg, QMessageBox.Yes, QMessageBox.No)
    return reply == QMessageBox.Yes
