import tkinter as tk
from gui.page import Page


class Page1(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        button = tk.Button(self, text='push me')
        button.pack(side='bottom')
