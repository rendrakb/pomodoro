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

    def __init__ (self, root: tk.Tk):
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

    def stop_timer(self):
        self.timer_running = False
        self.progress_bar["value"] = 0

    def pause_timer(self):
        self.timer_running = False
                    
class LayoutManager:
    def __init__(self, interface: PomodoroInterface):
        self.interface = interface
        self.root = self.interface.root

    def init_layout(self):
        self._time_entry_frame()
        self._buttons_frame()
        self._progress_bar_frame()
        self._status_frame()

    def _time_entry_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)
        
        row1 = ttk.Frame(frame)
        row1.pack(pady=3)

        work_label = ttk.Label(row1, text="Work:")
        work_label.pack(side="left", padx=3)

        self.interface.work_time_entry = ttk.Entry(row1, width=3)
        self.interface.work_time_entry.insert(0, "25")
        self.interface.work_time_entry.pack(side="left", padx=3)

        break_label = ttk.Label(row1, text="Break:")
        break_label.pack(side="left", padx=3)

        self.interface.break_time_entry = ttk.Entry(row1, width=3)
        self.interface.break_time_entry.insert(0, "5")
        self.interface.break_time_entry.pack(side="left", padx=1)

        row2 = ttk.Frame(frame)
        row2.pack(pady=3)

        longbreak_label = ttk.Label(row2, text="Longbreak:")
        longbreak_label.pack(side="left", padx=3)

        self.interface.longbreak_time_entry = ttk.Entry(row2, width=3)
        self.interface.longbreak_time_entry.insert(0, "15")
        self.interface.longbreak_time_entry.pack(side="left", padx=3)

        iterations_label = ttk.Label(row2, text="Iterations:")
        iterations_label.pack(side="left", padx=3)

        self.interface.iterations_entry = ttk.Entry(row2, width=3)
        self.interface.iterations_entry.insert(0, "4")
        self.interface.iterations_entry.pack(side="left", padx=3)

    def _buttons_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)

        self.interface.start_button = ttk.Button(frame, text="Start")
        self.interface.pause_button = ttk.Button(frame, text="Pause")
        self.interface.stop_button = ttk.Button(frame, text="Stop")

        self.interface.start_button.pack(side="left", padx=1)
        self.interface.pause_button.pack(side="left", padx=1)
        self.interface.stop_button.pack(side="left", padx=1)

    def _progress_bar_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)

        self.interface.progress_bar = ttk.Progressbar(frame,
        orient="horizontal", length=225, mode="determinate")
        self.interface.progress_bar.pack(pady=1)

    def _status_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)

def run():
    root = tk.Tk()

    root.title("Pomodoro")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"500x500+{(screen_width - 500) // 2}+{(screen_height - 500) // 2}")

    app = PomodoroInterface(root)

    root.mainloop()

if __name__ == "__main__":
    run()
