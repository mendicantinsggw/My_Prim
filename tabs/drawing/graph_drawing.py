import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx


class GraphDrawing(FigureCanvas):
    def __init__(self, G):
        self.figure = plt.figure()
        super().__init__(self.figure)
        self.G = G
        self.redraw()

    def redraw(self):
        self.figure.clf()

        pos = nx.spring_layout(self.G)  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(self.G, pos)  # connectionstyle="arc3,rad=0.1"

        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)

        self.draw_idle()
