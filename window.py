from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
import matplotlib.pyplot as plt
import networkx as nx
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from tabs.command_line.ui import CommandLineUi
from tabs.drawing.graph_drawing import GraphDrawing as GraphDrawing


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prim's algorithm")
        self.resize(600, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.G = nx.Graph()

        tabs = QTabWidget()
        drawing = GraphDrawing(self.G)
        tabs.addTab(CommandLineUi(drawing, self.G), "Terminal")
        tabs.addTab(drawing, "Canvas")
        layout.addWidget(tabs)
