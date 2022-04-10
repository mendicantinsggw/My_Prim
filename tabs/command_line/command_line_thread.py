from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit

from tabs.command_line.command import Command


class CommandLineThread(QThread):
    line_printed = pyqtSignal(str)

    def __init__(self, CmdUi):
        super().__init__(CmdUi)
        self.drawing = CmdUi.drawing

    def start_message(self):
        self.line_printed.emit("type 'help' to get all commands\n")

    def run(self, input_line: QLineEdit, G):  # line might have another type(?)
        command = Command(input_line, G, self.drawing, self.line_printed)
        command.run()
        input_line.setText("")
