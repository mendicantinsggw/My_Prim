from PyQt5.QtCore import QThread, pyqtSignal


class CommandLineThread(QThread):
    line_printed = pyqtSignal(str)

    def __init__(self, parent):
        super(CommandLineThread, self).__init__(parent)
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
