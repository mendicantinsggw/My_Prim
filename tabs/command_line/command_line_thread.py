from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from tabs.command_line.key_event_thread import TypeCommandEventThread
from tabs.command_line.command import Command


class CmdInputHandler(QThread):
    printed_line = pyqtSignal(str)
    command_to_execute = pyqtSignal(str)

    def __init__(self, CmdUi):
        super().__init__(CmdUi)
        self.drawing = CmdUi.drawing
        self.printed_line.emit("type 'help' to get all commands\n")
        TypeCommandEventThread(lambda: self.run_cmd(CmdUi.input_line.text()))

    def run_cmd(self, command: str):
        self.command_to_execute.emit(command)
