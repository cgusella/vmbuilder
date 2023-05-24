import constants
import customtkinter as ctk
from PIL import Image


class ErrorMessage(ctk.CTkToplevel):
    def __init__(self, master, message: str):
        ctk.CTkToplevel.__init__(self, master)
        self.geometry(
            '500x200'
        )
        self.title('Error')
        self.set_grid()
        error_image = ctk.CTkImage(
            Image.open(
                f"{constants.GUI_PATH}/views/errors/red-cross.png"
            ),
            size=(80, 80)
        )
        image_label = ctk.CTkLabel(
            self,
            image=error_image,
            text='',
        )
        my_font = ctk.CTkFont(
            family='DejaVu Sans',
            size=20
        )
        image_label.grid(row=0, column=0)
        text_label = ctk.CTkLabel(
            self,
            text=message,
            font=my_font
        )
        text_label.grid(row=1, column=0)

        ok_button = ctk.CTkButton(
            self,
            text='Ok',
            command=self.close_window
        )
        ok_button.grid(row=2, column=0)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def close_window(self):
        self.destroy()
