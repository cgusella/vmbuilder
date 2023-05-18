import tkinter as tk
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView


class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        self.provisions_configs = dict()
        tk.Frame.__init__(self, *args, **kwargs)
        self.vagrant_button = tk.Button(self, text='Vagrant',
                                        command=self.go_to_vagrant_page)
        packer_button = tk.Button(self, text='Packer',
                                  command=self.go_to_packer_page)

        self.vagrant_button.pack()
        packer_button.pack()

        exit_button = tk.Button(self, text='exit', command=self.close_window)
        exit_button.pack(side='bottom', anchor='s')

    def go_to_vagrant_page(self):
        self.vagrant_view = VagrantConfigsView(self)
        self.provisions_configs = self.vagrant_view.get_vagrant_configs()
        self.vagrant_view.geometry("400x300")

    def go_to_packer_page(self):
        pass

    def get_provisions_config(self):
        return self.provisions_configs

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.master.title('HackTheMonkey')
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x90")
    root.mainloop()
    print(main.provisions_configs)
