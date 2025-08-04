import sys

try:
    import tkinter as tk
    from tkinter import ttk

except (ModuleNotFoundError, ImportError):
    print(
        "Your Python environment does not have the required libraries installed."
    )
    sys.exit(0)

class PomodoroInterface:
    work_time_entry: ttk.Entry
    break_time_entry: ttk.Entry
    longbreak_time_entry: ttk.Entry
    iterations_entry: ttk.Entry
    start_button: ttk.Button
    stop_button: ttk.Button
    pause_button: ttk.Button
    progress_bar: ttk.Progressbar
    time_elapsed_label: ttk.Label
    time_left_label: ttk.Label
    iterations_left_label: ttk.Label
    status: ttk.Label

    def __init__ (self, root: tk.TK):
        self.root = root

        self.layout = LayoutManager(self)
        self.layout.init_layout()

        self.start_button.config(command=self.start_timer)
        self.stop_button.config(command=self.stop_timer)
        self.pause_button.config(command=self.pause_timer)
        self.timer_running = False

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True

class LayoutManager:
    def __init__(self, interface: MeditationInterface):
        self.interface = interface
        self.root = self.interface.root

    def init_layout(self):
        self._time_entry_frame()
        self._buttons_frame()
        self._progress_bar_frame()
        self._status_frame()