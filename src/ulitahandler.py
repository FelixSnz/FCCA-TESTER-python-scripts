
import subprocess
import pyautogui
import time



START_BTN_POS = (100,115)
serial_n_input_pos = (1540, 850)

class ProgramHandler():
    def __init__(self, program_name, program_cwd) -> None:
        self.name = program_name
        self.program_cwd = program_cwd
        self.process = None
        self.opened = False
        self.busy = False
    
    def open(self):
        self.process = subprocess.Popen(["cmd", "/c", "start", "/max", self.name], cwd=self.program_cwd, shell=True)
        self.opened = True
    
    def click(self, pos):
        pyautogui.click(pos)

    def typewrite(self, msg):
        print("tiping")
        pyautogui.typewrite(msg)
    
    def close(self):
        kill = "TaskKill /IM {} /F".format(self.name + ".exe")
        res = subprocess.run(kill)
        self.opened = False
    
    def is_opened(self):
        return self.opened
    






