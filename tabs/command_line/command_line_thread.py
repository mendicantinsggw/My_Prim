from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from tabs.command_line.key_event_thread import TypeCommandEventThread
from tabs.command_line.command import Command


class CmdInputHandler(QThread):
    printed_line = pyqtSignal(str)

    def __init__(self, CmdUi):
        super().__init__(CmdUi)
        self.drawing = CmdUi.drawing
        self.printed_line.emit("type 'help' to get all commands\n")
        TypeCommandEventThread(lambda: self.run_cmd(CmdUi.input_line, CmdUi.G))

    def run_cmd(self, input_line: QLineEdit, G):  # line might have another type(?)
        command = Command(input_line, G, self.drawing, self.printed_line)
        command.run()
        input_line.setText("")
