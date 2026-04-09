"""
Tab Controller - A simple single tab page
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class TabController(ABC):
    """Base class for tabs"""
    
    def __init__(self, notebook: ttk.Notebook, title: str):
        """
        :param notebook: The notebook widget
        :param title: The title of the tab
        """
        self.notebook = notebook
        self.title = title
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=title)
        
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        """Set up the UI - to be implemented by subclasses"""
        pass

    def refresh(self):
        """Refresh data - to be implemented by subclasses"""
        pass