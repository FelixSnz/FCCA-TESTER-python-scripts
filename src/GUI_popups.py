from tkinter import Tk, Entry, Frame, Button, Label, StringVar, messagebox, Toplevel
from tkinter import LEFT, X, Y, NW, CENTER, TOP, BOTTOM, TRUE, GROOVE, RIGHT
from sys import exc_info, exit
import os
import time

quit_confirmed = False

current_windows = []
can_destroy = False


class MainApplication(Frame):
    def __init__(self, root, *args, **kwargs):
        Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.serial = ""
        self.askserial_window = None
    
    def wait_window_destroy(self, window):
        self.root.wait_window(window)
    
    def on_close_ask_serial(self, wd):
        self.serial = None
        wd.destroy()

    
    def ask_serial(self):
        askserial_window = Toplevel(self.root)
        askserial_window.attributes('-topmost',True)
        self.askserial_window = askserial_window
        askserial_window.protocol("WM_DELETE_WINDOW", lambda:self.on_close_ask_serial(askserial_window))
        
        askserial_window.geometry("1200x250")
        top_frame_right_upper = Frame(askserial_window, bg='gray94', highlightthickness=2)
        
        top_frame_right_upper.pack(side=LEFT)
        path_label = Label(top_frame_right_upper, text='Serial: ', bg='gray94', font="Arial 18")
        
        path_label.pack(side=LEFT)
        textEntryPath = StringVar()
        pathEntry = Entry(top_frame_right_upper, textvariable=textEntryPath, bg='white', font="Arial 24")
        
        pathEntry.pack(side=LEFT, fill=X, expand=True)
        print(pathEntry.focus)

        askserial_window.focus_set()
        pathEntry.focus_set()
        # pathEntry.focus_force()
        
        browse_btn = Button(top_frame_right_upper, text='Send', font="Arial 16", command=lambda:self.save_serial(textEntryPath.get()), padx=20)
        top_frame_right_upper.place(relx=.5, rely=.5, anchor="center")
        
        browse_btn.pack(side=LEFT,  anchor=NW)
        
        center(askserial_window)
        askserial_window.attributes('-alpha', 1.0)
        return askserial_window

    def message(self, message, bg_color, font_size=45, window_size = "1350x600"):
        root = Toplevel(self.root)
        root.geometry(window_size)
        root.configure(background=bg_color)

        message_frame = Frame(root, bg=bg_color)
        message_frame.pack()
        message_frame.place(relx=.5, rely=.5, anchor="center")

        message_label = Label(message_frame, text=message, bg=bg_color, font="Arial " + str(font_size)+ " bold")
        message_label.pack(side=TOP, expand=TRUE, fill=Y)

        ok_btn = Button(message_frame, text='Ok', font="Arial 35", command=lambda:destroy_self(root))
        ok_btn.pack(side=BOTTOM)
        center(root)

        root.attributes('-alpha', 1.0)
        return root
    
    def save_serial(self, serial=""):
        self.serial = serial
        self.askserial_window.destroy()
     





def debug():
    # try:
    #     raise Exception('spam', 'eggs')
    # except Exception as e:
    #     show_error(e, "titulo")
    # operator_message("asddddddddddddaddasdad\nasdadasdadasd\nasdaddadadadasdad\nasdsadadad", "green")
    time.sleep(100)

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    win.deiconify()

def destroy_enabled():
    global can_destroy
    can_destroy = True

def show_error(e, tittle_error):
        exc_type, exc_obj, exc_tb = exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2} \n \
    in file: {3}".format(e, exc_type, exc_tb.tb_lineno, os.path.basename(__file__))
        messagebox.showerror(tittle_error, error)


def try_to_destroy(root):
    global can_destroy
    if can_destroy:
        root.destroy()


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()



def destroy_self(root):
    root.destroy()
    

    pass

def destroy_current_windows():
    for window in current_windows:
        window.mainloop()
        window.destroy()
        


def on_quit_response(resp, root):
    global quit_confirmed
    if resp == "si":
        quit_confirmed = True
        
    elif resp == "no":
        quit_confirmed = False
    root.destroy()
    

def ask_quit():
    global quit_confirmed
    root = Tk()


    root.title("Salir")
    label = Label(root, text="Seguro que quiere salir?",
                  font=("ariel 22 bold"), justify=LEFT)
    label.pack(padx=20, pady=15)
    no = Button(root, text="No", font=("ariel 15 bold"), width=8, relief=GROOVE,
                bd=3, command=lambda: on_quit_response("no", root))
    no.pack(padx=5, pady=10, side=RIGHT)
    yes = Button(root, text="Si", font=("ariel 15 bold"), width=8, relief=GROOVE,
                 bd=3, command=lambda: on_quit_response("si", root))
    yes.pack(pady=10, side=RIGHT)
    center(root)
    root.lift()
    root.attributes("-topmost", True)

    root.mainloop()

    return quit_confirmed





if __name__ == '__main__':
    # ask_quit()
    debug()
