from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit

from tabs.network_drawing import network_tab_ui
from tabs.command_line.command import Command


class CommandLineThread(QThread):
    line_printed = pyqtSignal(str)

    def __init__(self, drawing: network_tab_ui):
        super(CommandLineThread, self).__init__(drawing)
        self.drawing = drawing

    def start_message(self):
        self.line_printed.emit("type 'help' to get all commands\n")

    def run(self, line: QLineEdit, G):  # line might have another type(?)
        command = Command(line, G, self.drawing, self.line_printed)
        command.run()
