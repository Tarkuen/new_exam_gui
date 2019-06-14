import tkinter as tk
from tkinter import filedialog


class ClientWindow:

    def __init__(self, controller):

        self.controller = controller

        # Main Window 
        self.top = tk.Tk()
    
        self.top.title("TCP Client")
        self.top.geometry('500x600')
        self.top.protocol("WM_DELETE_WINDOW", self.close_all)

        self.top.bind('<Escape>', self.close_all)
        self.msg_frame = tk.Frame(self.top)
        self.my_msg = tk.StringVar()
        self.my_msg.set("Type here")
        self.scrollbar = tk.Scrollbar(self.msg_frame)

        # Chat Window
        self.msg_list = tk.Listbox(self.msg_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(fill="both", expand=True)
        self.msg_frame.pack(fill=tk.BOTH, expand=1)

        # Input Window 
        self.entry_field = tk.Entry(self.top, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.controller.send)
        self.entry_field.pack()
        self.send_button = tk.Button(self.top, text="Send Msg", command=self.controller.send)
        self.send_button.pack()

    def openfile(self):

        f = tk.filedialog.askopenfilename( 
            parent=self.top, initialdir='C:/', title='Choose file',
            filetypes=[('png images', '.png'),('gif images', '.gif'),("all files","*.*")]
            )
            
        return f

    def close_all(self, event=None):
        self.top.destroy()
        self.top.quit()

 