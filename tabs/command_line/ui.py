import networkx as nx
from PyQt5.QtWidgets import QDialog, QTextEdit, QLineEdit, QVBoxLayout

from tabs.command_line.command_line_thread import CmdInputHandler
from tabs.drawing.graph_drawing import GraphDrawing
from tabs.command_line.command import  Command


class CommandLineUi(QDialog):
    def __init__(self, drawing: GraphDrawing, G: nx.Graph):
        super().__init__()
        self.G = G
        self.drawing = drawing
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.input_line = QLineEdit('', self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.input_line)

        self.input_handler = CmdInputHandler(self)
        self.input_handler.command_to_execute.connect(self.run_cmd)
        self.input_handler.printed_line.connect(self.handle_line)

    def run_cmd(self, command: str):  # line might have another type(?)
        command = Command(self.input_line, self.G, self.drawing, self.handle_line)
        self.input_line.setText("")
        command.run()

    def handle_line(self, line):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.textEdit.ensureCursorVisible()