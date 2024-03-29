import json
import os

import tkinter as tk
from threading import Thread

import ma2.view
import ma2.model

from protocol import Protocol


class TCPController:

    def __init__(self):
        self.model = ma2.model.TCPClient()
        self.view = ma2.view.ClientWindow(self)
        self.protocol = Protocol()
        self.keywords = self.protocol.getKeywords()
        self.listener = Thread(target=self.recieve)
        self.listener.start()
        self.view.top.mainloop()


    def send(self, event=None):

        msg = self.view.my_msg.get()

        for k, v in self.keywords.items():
            if k in msg:
                keyword_method = getattr(self, str(v))(msg=msg)
 
        self.view.my_msg.set("")

    def handle_quit(self, **kwargs):
        self.model.shutdown()
        self.view.top.quit()

    def handle_broadcast(self, **kwargs):
        if (kwargs.__contains__('msg')):
            msg = kwargs.get('msg')
        else:
            msg = ''


        a = self.model.send(msg)
        if a == -1:
            self.view.top.destroy()

    def handle_file(self, **kwargs):
        if (kwargs.__contains__('msg')):
            msg = kwargs.get('msg')
        else:
            msg = ''

        path = self.view.openfile()
        file_size = os.path.getsize(path)
        file_encoding = str(path.split('.', 1)[-1])
        file_msg = msg + "_" + str(file_size) + "_" + file_encoding

        self.model.send(file_msg)
        a = self.model.sendFile(path=path, my_msg=msg)
        self.view.msg_list.insert(tk.END, a)

    def recieve(self):

        protocol = str( [(k+' ') for k  in self.keywords.keys()])
        self.view.msg_list.insert(tk.END, f"Current protocols are: {protocol}")
        self.view.msg_list.insert(tk.END, "Private Messages are sent with { TARGET USER, TARGET...} after protocol keyword")
        self.view.msg_list.insert(tk.END, "Select a username with '@broadcast USERNAME' with no spaces")
        while True:
            msg = self.model.receive()
            if msg == -1:
                break
            self.view.msg_list.insert(tk.END, msg)
            self.view.msg_list.yview_scroll(1, "units")
