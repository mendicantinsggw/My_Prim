import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx


class GraphDrawing(FigureCanvas):
    def __init__(self, G: nx.Graph):
        self.figure = plt.figure()
        super().__init__(self.figure)
        self.G = G
        self.redraw()

    def redraw(self):
        self.figure.clf()

        pos = nx.spring_layout(self.G, k=0.5, iterations=20)  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(self.G, pos)  # connectionstyle="arc3,rad=0.1"

        labels = nx.get_edge_attributes(self.G, 'weight')
        colors = list(nx.get_edge_attributes(self.G, 'color').values())
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)

        nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(), edge_color=colors)

        self.draw_idle()

    def clear(self):
        self.G.clear()
        self.redraw()
