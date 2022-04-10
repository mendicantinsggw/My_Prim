import networkx as nx
from PyQt5.QtWidgets import QDialog, QTextEdit, QLineEdit, QVBoxLayout

from tabs.command_line.key_event_thread import KeyEventThread
from tabs.command_line.command_line_thread import CommandLineThread
from tabs.drawing.graph_canvas import GraphCanvas


class CommandLineUi(QDialog):
    def __init__(self, canvas: GraphCanvas, G: nx.Graph):
        super().__init__()
        self.G = G
        self.canvas = canvas
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.lineEdit = QLineEdit('', self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.lineEdit)

        KeyEventThread(self.run_thread)
        self.thread = CommandLineThread(self)
        self.thread.line_printed.connect(self.handle_line)
        self.thread.start_message()

    def run_thread(self):
        self.thread.run(self.lineEdit, self.G)

    def handle_line(self, line):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.textEdit.ensureCursorVisible()