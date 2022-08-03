from pynput import keyboard
from GUI_popups import ask_quit, destroy_enabled
import sys, os
from concurrent import futures

#hotkey o comando para cerrar el programa es shift + esc

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)

COMBINATIONS = [
    {keyboard.Key.shift, keyboard.Key.esc}
]

current = set()


class CloseHotkeyWaiter():

    def __init__(self, program_to_close) -> None:
        self.program_to_close = program_to_close
        self.running = True
    
    def start(self):
        thread_pool_executor.submit(self.listening_hotkey)

    def on_hotkey(self):

        if not self.program_to_close.busy:
            if ask_quit():
                self.program_to_close.close()
                os._exit(1)
                
            

    def on_press(self, key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
                self.on_hotkey()

    def on_release(self, key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.remove(key)

    def listening_hotkey(self, ):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def is_running(self):
        return self.running





