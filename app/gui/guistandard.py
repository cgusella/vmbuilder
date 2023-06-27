import abc
import customtkinter as ctk


class GuiStandard(abc.ABC, ctk.CTkFrame):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def set_fonts(self):
        pass

    @abc.abstractmethod
    def set_std_dimensions(self):
        pass

    @abc.abstractmethod
    def initialize_elements(self):
        pass

    @abc.abstractmethod
    def render_elements(self):
        pass


class GuiStandardValues(GuiStandard):

    @abc.abstractmethod
    def initialize_values(self):
        pass

    @abc.abstractmethod
    def render_values(self):
        pass
