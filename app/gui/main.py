import tkinter as tk
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView


class MainView(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.vagrant_button = tk.Button(self, text='Vagrant',
                                        command=self.go_to_vagrant_page)
        self.packer_button = tk.Button(self, text='Packer',
                                       command=self.go_to_packer_page)

        self.vagrant_button.grid(row=0, column=1)
        self.packer_button.grid(row=1, column=1)

        exit_button = tk.Button(self, text='exit', command=self.close_window)
        exit_button.grid(row=2, column=1)

    def go_to_vagrant_page(self):
        VagrantConfigsView(self)

    def go_to_packer_page(self):
        pass

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("400x200")
    main = MainView(root)
    main.master.title('HackTheMonkey')
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
