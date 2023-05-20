import tkinter as tk
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView


class MainView(tk.Frame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
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
        self.vagrant_view = VagrantConfigsView(self, self.provisions_configs)
        self.provisions_configs = self.vagrant_view.get_vagrant_configs()
        self.vagrant_view.geometry("400x300")

    def go_to_packer_page(self):
        pass

    def get_provisions_config(self):
        return self.provisions_configs

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    provisions_configs = {
        'packages_to_install': [],
        'packages_to_uninstall': [],
        'packages_to_config': [],
    }
    root = tk.Tk()
    root.wm_geometry("400x200")
    main = MainView(root, provisions_configs)
    main.master.title('HackTheMonkey')
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
    print(main.get_provisions_config())
