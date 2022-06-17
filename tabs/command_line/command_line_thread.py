from PyQt5.QtCore import QThread, pyqtSignal
from tabs.command_line.key_event_thread import TypeCommandEventThread


class CmdInputHandler(QThread):
    printed_line = pyqtSignal(str)
    command_to_execute = pyqtSignal(str)

    def __init__(self, CmdUi):
        super().__init__(CmdUi)
        self.drawing = CmdUi.drawing
        TypeCommandEventThread(lambda: self.run_cmd(CmdUi.input_line.text()))

    def run_cmd(self, command: str):
        self.command_to_execute.emit(command)
