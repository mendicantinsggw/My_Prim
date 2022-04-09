import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import threading
from pynput.keyboard import Listener, Key


class KeyEventThread(threading.Thread):
    def __init__(self, run_cmd):
        super().__init__()
        self.run_cmd = run_cmd
        self.listner = Listener(on_press=self.on_press)
        self.listner.start()

    def on_press(self, key):
        if key == Key.enter:
            self.run_cmd()


class MyThread(QThread):
    line_printed = pyqtSignal(str)

    def __init__(self, parent):
        super(MyThread, self).__init__(parent)
        self.parent = parent
        self.cmd = None

    def start_message(self):
        self.line_printed.emit(
            "type 'help' to get all commands\n".format(self.cmd))

    def run(self, line, B):
        try:
            self.cmd = line.text()
        except:
            self.cmd = line

        self.line_printed.emit("> " + self.cmd + "\n")
        if self.cmd:
            commands = self.cmd.split()

            if commands[0] == "add":
                if len(commands) == 2:
                    if not B.has_node(commands[1]):
                        self.parent.add_node_and_generate(commands[1])
                    else:
                        self.line_printed.emit("this node already exist\n")
                else:
                    self.line_printed.emit("only one id must be\n")

            elif commands[0] == "delete":
                if len(commands) == 2:
                    if B.has_node(commands[1]):
                        self.parent.remove_node_and_generate(commands[1])
                    else:
                        self.line_printed.emit("this node doesnt't exist\n")
                else:
                    self.line_printed.emit("only one id must be\n")

            elif commands[0] == "connect":
                if len(commands) == 4:
                    if B.has_node(commands[1]) and B.has_node(commands[2]) and not B.has_edge(commands[1], commands[2]):
                        self.parent.add_edge_and_generate(
                            commands[1], commands[2], int(commands[3]))
                    else:
                        self.line_printed.emit(
                            "nodes don't exist or edge already exist\n")
                else:
                    self.line_printed.emit("two ids must be\n")

            elif commands[0] == "delconnect":
                if len(commands) == 3:
                    if B.has_node(commands[1]) and B.has_node(commands[2]) and B.has_edge(commands[1], commands[2]):
                        self.parent.remove_edge_and_generate(
                            commands[1], commands[2])
                    else:
                        self.line_printed.emit(
                            "nodes don't exist or edge doesn't exist\n")
                else:
                    self.line_printed.emit("two ids must be\n")

            elif commands[0] == "prim":
                if len(commands) == 2:
                    if B.has_node(commands[1]):
                        self.parent.prims_algoritm(commands[1])
                else:
                    self.line_printed.emit("one id must be\n")

            elif commands[0] == "readfrom":
                if len(commands) == 2:
                    try:
                        file = open(commands[1], 'r').read()
                        lines = file.split('\n')
                        for line in lines:
                            self.run(line, B)
                    except:
                        self.line_printed.emit(
                            "Some error with data in file\n")
                else:
                    self.line_printed.emit("one id must be\n")

            elif commands[0] == "refresh":
                if len(commands) == 1:
                    self.parent.refresh()

            elif self.cmd == "help":
                self.line_printed.emit(
                    "~ add id \n~ delete id \n~ connect id1 id2 weight \n~ delconnect id1 id2 \n~ prim id \n~ readfrom file.txt \n~ refresh \n")

            else:
                self.line_printed.emit("There is no command like that\n")

        else:
            self.line_printed.emit("What did you write ? O_o\n")


class MyDialog(QDialog):
    def __init__(self, U, B):
        super().__init__()
        self.B = B
        self.U = U
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.lineEdit = QLineEdit('', self)
        KeyEventThread(self.run_thread)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.lineEdit)

        self.thread = MyThread(self)
        self.thread.line_printed.connect(self.handle_line)

        self.thread.start_message()

    def add_node_and_generate(self, id):
        self.B.add_node(id)
        self.U.generate_tab_ui()

    def remove_node_and_generate(self, id):
        self.B.remove_node(id)
        self.U.generate_tab_ui()

    def add_edge_and_generate(self, id1, id2, new_weight):
        self.B.add_edge(id1, id2, weight=new_weight)
        self.U.generate_tab_ui()

    def remove_edge_and_generate(self, id1, id2):
        self.B.remove_edge(id1, id2)
        self.U.generate_tab_ui()

    def prims_algoritm(self, id):
        H = nx.Graph()
        H.add_nodes_from(sorted(self.B.nodes(data=True)))
        H.add_edges_from(self.B.edges(data=True))
        self.B = H
        self.refresh()

        A = nx.adjacency_matrix(self.B)
        INF = 10000
        V = len(A.toarray())
        G = A.toarray()
        selected = [0] * len(A.toarray())
        no_edge = 0
        print(list(self.B.nodes()))
        selected[list(self.B.nodes()).index(id)] = True
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
            self.thread.line_printed.emit(
                str(x) + "-" + str(y) + ":" + str(G[x][y]) + "\n")
            print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
            selected[y] = True
            no_edge += 1
        self.U.generate_tab_ui()

    def refresh(self):
        self.U.generate_tab_ui()

    def run_thread(self):
        self.thread.run(self.lineEdit, self.B)

    def handle_line(self, line):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.textEdit.ensureCursorVisible()


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
        tabs.addTab(self.network_tab_ui(), "Terminal")
        tabs.addTab(self.generate_tab_ui(), "Canvas")

        layout.addWidget(tabs)

    def generate_tab_ui(self):
        self.figure.clf()

        pos = nx.spring_layout(self.B, k=self.B.number_of_nodes())  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(self.B, pos)
        labels = nx.get_edge_attributes(self.B, 'weight')
        nx.draw_networkx_edge_labels(self.B, pos, edge_labels=labels)
        self.canvas.draw_idle()
        return self.canvas

    def network_tab_ui(self):
        dlg = MyDialog(self, self.B)
        return dlg