from typing import Callable

import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from networkx import Graph

from tabs.drawing.graph_drawing import GraphDrawing


class Command:
    def __init__(self, text_line: str | QLineEdit, G: Graph, drawing: GraphDrawing, handle_line: Callable):
        self.function: str = None
        self.args: list[str] = []
        self.set(text_line)
        self.G = G
        self.drawing = drawing
        self.handle_line = handle_line

    def set(self, text_line: str | QLineEdit):
        try:
            command_text = text_line.text().split()
        except AttributeError:
            command_text = text_line.split()

        if len(command_text) >= 1:
            self.function = command_text[0]
            self.args = command_text[1:]

    def run(self, redraw=True):
        if self.function is None: return

        self.handle_line(f"> {self.function} {' '.join(self.args)}\n")
        if self.function == "add":
            self.__add()
        elif self.function == "delete":
            self.__delete()
        elif self.function == "connect":
            self.__connect()
        elif self.function == "delconnect":
            self.__delconnect()
        elif self.function == "prim":
            self.__prim_algorithm()
        elif self.function == "readfrom":
            self.__readfrom()
        elif self.function == "refresh":
            self.__refresh()
        elif self.function == "help":
            self.__print_help()
        elif self.function == "clear":
            self.__clear_graph()
        else:
            self.__print_syntax_error()

        if redraw: self.drawing.redraw()

    def __add(self):
        if len(self.args) != 1:
            self.handle_line("only one id must be provided\n")
            return

        if not self.G.has_node(self.args[0]):
            self.G.add_node(self.args[0], color='b')
        else:
            self.handle_line("this node already exist\n")

    def __delete(self):
        if len(self.args) != 1:
            self.handle_line("only one id must be provided\n")
            return

        if self.G.has_node(self.args[0]):
            self.G.remove_node(self.args[0])
        else:
            self.handle_line("this node doesnt't exist\n")

    def __connect(self):
        if len(self.args) != 3:
            self.handle_line("two ids must be provided\n")
            return

        if self.G.has_node(self.args[0]) and self.G.has_node(self.args[1]) and not self.G.has_edge(self.args[0], self.args[1]):
            self.G.add_edge(
                self.args[0], self.args[1], weight=int(self.args[2]), color="black"
            )
        else:
            self.handle_line("nodes don't exist or edge already exist\n")

    def __delconnect(self):
        if len(self.args) != 2:
            self.handle_line("two ids must be provided\n")
            return

        if self.G.has_edge(self.args[0], self.args[1]):
            self.G.remove_edge(self.args[0], self.args[1])
        else:
            self.handle_line("nodes don't exist or edge doesn't exist\n")

    def __prim_algorithm(self):
        if len(self.args) == 1:
            chosen_edges = []
            node_names = list(self.G.nodes())
            if self.G.has_node(self.args[0]):
                H = nx.Graph()
                H.add_nodes_from(sorted(self.G.nodes(data=True)))
                H.add_edges_from(self.G.edges(data=True))
                self.G = H

                A = nx.adjacency_matrix(self.G)
                # A = nx.to_numpy_matrix(self.G, nonedge=None).tolist()
                INF = 10000
                V = len(A.toarray())
                G = nx.to_numpy_matrix(self.G, nonedge=None).tolist()
                selected = [0] * len(A.toarray())
                no_edge = 0
                print(list(self.G.nodes()))
                selected[list(self.G.nodes()).index(self.args[0])] = True
                while no_edge < V - 1:
                    minimum = INF
                    x = 0
                    y = 0
                    for i in range(V):
                        if selected[i]:
                            for j in range(V):
                                if (not selected[j]) and G[i][j] is not None:
                                    if minimum > G[i][j]:
                                        minimum = G[i][j]
                                        x = i
                                        y = j
                    self.handle_line(
                        str(node_names[x]) + " - " + str(node_names[y]) + ": " + str(G[x][y]) + "\n")
                    print(str(node_names[x]) + "-" + str(node_names[y]) + ":" + str(G[x][y]))
                    chosen_edges.append((x, y))
                    selected[y] = True
                    no_edge += 1

                self.__color_edges(chosen_edges)
        else:
            self.handle_line("one id must be provided\n")

    def __color_edges(self, chosen_edges):
        old_G = self.drawing.G.copy()
        self.drawing.clear()
        edges = nx.adjacency_matrix(self.G).toarray()
        node_names = list(self.G.nodes())

        for node in node_names:
            self.drawing.G.add_node(str(node))

        for edge in chosen_edges:
            self.drawing.G.add_edge(node_names[edge[0]], node_names[edge[1]], color='r', weight=edges[edge[0]][edge[1]])

        old_edges = list()
        old_matrix = nx.to_numpy_matrix(self.G, nonedge=None).tolist()
        for x in range(len(old_matrix)):
            for y in range(len(old_matrix)):
                if old_matrix[x][y] is not None and not self.drawing.G.has_edge(node_names[x], node_names[y]):
                    old_edges.append((x, y))

        for edge in old_edges:
            if not self.drawing.G.has_edge(edge[0], edge[1]):
                self.drawing.G.add_edge(node_names[edge[0]], node_names[edge[1]], color='black', weight=edges[edge[0]][edge[1]])

    def __readfrom(self):
        if len(self.args) != 1:
            self.handle_line("one id must be provided\n")
            return
        lines = ""
        try:
            file = open(self.args[0], 'r')
            lines = file.read().split("\n")
            file.close()

        except IOError:
            self.handle_line("Some error with data in file\n")

        for line in lines:
            self.set(line)
            self.run(redraw=False)
        self.drawing.redraw()

    def __refresh(self):
        if len(self.args) != 0:
            self.handle_line("Refresh doesn't take any arguments")
            return

        self.drawing.redraw()

    def __print_help(self):
        self.handle_line(
            "~ add id \n~ delete id \n~ connect id1 id2 weight \n~ delconnect id1 id2 \n~ prim id \n~ readfrom file.txt \n~ refresh \n~ clear \n")

    def __print_syntax_error(self):
        self.handle_line("There is no command like that\n")

    def __clear_graph(self):
        if len(self.args) != 0:
            self.handle_line("Clear doesn't take any arguments")
        else:
            self.drawing.clear()
