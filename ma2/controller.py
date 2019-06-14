import json

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

        if msg == self.keywords.get('@quit'):
            self.model.shutdown()
            self.view.top.quit()

        else:
            if msg.find(self.keywords.get('@file')) != -1:
                path = self.view.openfile()
                a = self.model.sendFile(path=path, my_msg=msg)
                self.view.msg_list.insert(tk.END, a)
            else:
                a = self.model.send(msg)
                if a == -1:
                    self.view.top.destroy()

        self.view.my_msg.set("")

    def recieve(self):

        protocol = str( [(k+' ') for k  in self.keywords.keys()])
        self.view.msg_list.insert(tk.END, "Current protocols are: "+ protocol)
        while True:
            msg = self.model.receive()
            if msg == -1:
                break
            self.view.msg_list.insert(tk.END, msg)
            self.view.msg_list.yview_scroll(1, "units")
