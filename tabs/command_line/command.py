import networkx as nx
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from networkx import Graph

from tabs.drawing.graph_drawing import GraphDrawing


class Command:
    def __init__(self, text_line: str | QLineEdit, G: Graph, drawing: GraphDrawing, line_printed: pyqtSignal):
        self.function: str = None
        self.args: list[str] = []
        self.set(text_line)
        self.G = G
        self.drawing = drawing
        self.line_printed = line_printed

    def set(self, text_line: str | QLineEdit):
        try:
            command_text = text_line.text().split()
        except AttributeError:
            command_text = text_line.split()

        if len(command_text) >= 1:
            self.function = command_text[0]
            self.args = command_text[1:]

    def run(self, redraw=True):
        self.line_printed.emit(f"> {self.function} {' '.join(self.args)}\n")
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
        else:
            self.__print_syntax_error()

        if redraw: self.drawing.redraw()

    def __add(self):
        if len(self.args) != 1:
            self.line_printed.emit("only one id must be\n")
            return

        if not self.G.has_node(self.args[0]):
            self.G.add_node(self.args[0])
        else:
            self.line_printed.emit("this node already exist\n")

    def __delete(self):
        if len(self.args) != 1:
            self.line_printed.emit("only one id must be\n")
            return

        if self.G.has_node(self.args[0]):
            self.G.remove_node(self.args[0])
        else:
            self.line_printed.emit("this node doesnt't exist\n")

    def __connect(self):
        if len(self.args) != 3:
            self.line_printed.emit("two ids must be\n")
            return

        if self.G.has_node(self.args[0]) and self.G.has_node(self.args[1]) and not self.G.has_edge(self.args[0], self.args[1]):
            self.G.add_edge(
                self.args[0], self.args[1], weight=int(self.args[2])
            )
        else:
            self.line_printed.emit("nodes don't exist or edge already exist\n")

    def __delconnect(self):
        if len(self.args) != 2:
            self.line_printed.emit("two ids must be\n")
            return

        if self.G.has_edge(self.args[0], self.args[1]):
            self.G.remove_edge(self.args[0], self.args[1])
        else:
            self.line_printed.emit("nodes don't exist or edge doesn't exist\n")

    def __prim_algorithm(self):
        if len(self.args) != 1:
            if self.G.has_node(self.args[0]):
                H = nx.Graph()
                H.add_nodes_from(sorted(self.G.nodes(data=True)))
                H.add_edges_from(self.G.edges(data=True))
                self.G = H

                A = nx.adjacency_matrix(self.G)
                INF = 10000
                V = len(A.toarray())
                G = A.toarray()
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
                                if (not selected[j]) and G[i][j]:
                                    if minimum > G[i][j]:
                                        minimum = G[i][j]
                                        x = i
                                        y = j
                    self.line_printed.emit(
                        str(x) + "-" + str(y) + ":" + str(G[x][y]) + "\n")
                    print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
                    selected[y] = True
                    no_edge += 1
        else:
            self.line_printed.emit("one id must be\n")

    def __readfrom(self):
        if len(self.args) != 1:
            self.line_printed.emit("one id must be\n")
            return

        try:
            file = open(self.args[0], 'r')
            lines = file.read().split("\n")

            for line in lines:
                self.set(line)
                self.run(redraw=False)
        except IOError:
            self.line_printed.emit("Some error with data in file\n")
        self.drawing.redraw()

    def __refresh(self):
        if len(self.args) != 0:
            self.line_printed.emit("Refresh doesn't take any arguments")
            return

        self.drawing.redraw()

    def __print_help(self):
        self.line_printed.emit(
            "~ add id \n~ delete id \n~ connect id1 id2 weight \n~ delconnect id1 id2 \n~ prim id \n~ readfrom file.txt \n~ refresh \n")

    def __print_syntax_error(self):
        self.line_printed.emit("There is no command like that\n")
