"""
标签页控制器 - 简洁的单个标签页
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class TabController(ABC):
    """标签页基类"""
    
    def __init__(self, notebook: ttk.Notebook, title: str):
        """
        :param notebook: Notebook 控件
        :param title: 标签页标题
        """
        self.notebook = notebook
        self.title = title
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=title)
        
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        """设置 UI - 由子类实现"""
        pass

    def refresh(self):
        """刷新数据 - 由子类实现"""
        pass
