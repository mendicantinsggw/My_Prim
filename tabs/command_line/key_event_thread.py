from pynput.keyboard import Listener, Key


class TypeCommandEventThread():
    def __init__(self, run_cmd):
        super().__init__()
        self.run_cmd = run_cmd
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if key == Key.enter:
            self.run_cmd()
