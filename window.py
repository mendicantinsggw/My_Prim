from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

from network_tab_ui import NetworkTabUi


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prim's algorithm")
        self.resize(600, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.clf()
        self.B = nx.Graph()

        tabs = QTabWidget()
        tabs.addTab(NetworkTabUi(self, self.B), "Terminal")
        tabs.addTab(self.generate_tab_ui(), "Canvas")

        layout.addWidget(tabs)

    def generate_tab_ui(self):
        self.figure.clf()

        pos = nx.spring_layout(self.B)  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(self.B, pos)
        labels = nx.get_edge_attributes(self.B, 'weight')
        nx.draw_networkx_edge_labels(self.B, pos, edge_labels=labels)
        self.canvas.draw_idle()
        return self.canvas
