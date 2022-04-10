from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from networkx import Graph


class Command:
    def __init__(self, text_line: str, G: Graph, drawing, line_printed: pyqtSignal):
        self.function: str = None
        self.args: str = None
        self.set(text_line)
        self.G = G
        self.drawing = drawing
        self.line_printed = line_printed

    def set(self, text_line: str | QLineEdit):
        try:
            command_text = text_line.text().split()
        except AttributeError:
            command_text = text_line.split()

        self.function = command_text[0]
        self.args = command_text[1:]

    def run(self):
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

    def __add(self):
        if len(self.args) != 1:
            self.line_printed.emit("only one id must be\n")
            return

        if not self.G.has_node(self.args[0]):
            self.drawing.add_node_and_generate(self.args[0])
        else:
            self.line_printed.emit("this node already exist\n")

    def __delete(self):
        if len(self.args) != 1:
            self.line_printed.emit("only one id must be\n")
            return

        if self.G.has_node(self.args[0]):
            self.drawing.remove_node_and_generate(self.args[0])
        else:
            self.line_printed.emit("this node doesnt't exist\n")

    def __connect(self):
        if len(self.args) != 3:
            self.line_printed.emit("two ids must be\n")
            return

        if self.G.has_node(self.args[0]) and self.G.has_node(self.args[1]) and not self.G.has_edge(self.args[0], self.args[1]):
            self.drawing.add_edge_and_generate(
                self.args[0], self.args[1], int(self.args[2])
            )
        else:
            self.line_printed.emit("nodes don't exist or edge already exist\n")

    def __delconnect(self):
        if len(self.args) != 2:
            self.line_printed.emit("two ids must be\n")
            return

        if self.G.has_edge(self.args[0], self.args[1]):
            self.drawing.remove_edge_and_generate(
                self.args[0], self.args[1]
            )
        else:
            self.line_printed.emit("nodes don't exist or edge doesn't exist\n")

    def __prim_algorithm(self):
        if len(self.args) != 1:
            if self.G.has_node(self.args[0]):
                self.drawing.prims_algoritm(self.args[0])
        else:
            self.line_printed.emit("one id must be\n")

    def __readfrom(self):
        if len(self.args) != 1:
            self.line_printed.emit("one id must be\n")
            return

        try:
            file = open(self.args[0], 'r')
            lines = file.read().split()
            for line in lines:
                self.set(line)
                self.run()
        except IOError:
            self.line_printed.emit("Some error with data in file\n")

    def __refresh(self):
        if len(self.args) != 0:
            self.line_printed.emit("Refresh doesn't take any arguments")
            return

        self.drawing.refresh()

    def __print_help(self):
        self.line_printed.emit(
            "~ add id \n~ delete id \n~ connect id1 id2 weight \n~ delconnect id1 id2 \n~ prim id \n~ readfrom file.txt \n~ refresh \n")

    def __print_syntax_error(self):
        self.line_printed.emit("There is no command like that\n")
