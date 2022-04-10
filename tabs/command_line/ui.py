import networkx as nx
from PyQt5.QtWidgets import QDialog, QTextEdit, QLineEdit, QVBoxLayout

from tabs.command_line.key_event_thread import TypeCommandEventThread
from tabs.command_line.command_line_thread import CmdInputHandler
from tabs.drawing.graph_drawing import GraphDrawing


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
        self.input_handler.printed_line.connect(self.handle_line)

    def handle_line(self, line):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.textEdit.ensureCursorVisible()