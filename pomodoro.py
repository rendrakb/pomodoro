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
    status_label: ttk.Label
    phase_label: ttk.Label

    def __init__ (self, root: tk.Tk):
        self.root = root

        self.layout = LayoutManager(self)
        self.layout.init_layout()

        self.start_button.config(command=self.start_timer)
        self.stop_button.config(command=self.stop_timer)
        self.pause_button.config(command=self.pause_timer)
        self.timer_running = False

        self.state = "idle"
        self.time_remaining = 0
        self.timer_job = None

        self.current_iteration = 0
        self.total_iterations = 0
        self.current_phase = "work"

    def start_timer(self):
        if self.state == "running":
            return

        if self.state == "idle":
            try:
                self.total_iterations = int(self.iterations_entry.get())
                self.current_iteration = 0
            except ValueError:
                self.status_label.config(text="Invalid iterations input.")
                return

            self.current_phase = "work"
            self._set_phase_timer()
            self.status_label.config(text="Status: Running")

        self.state = "running"
        self._run_timer()

    def _run_timer(self):
        if self.state != "running":
            return

        mins, secs = divmod(self.time_remaining, 60)
        self.time_left_label.config(text=f"Time Left: {mins:02}:{secs:02}")

        if self.current_phase == "work":
            total_time = int(self.work_time_entry.get()) * 60
        elif self.current_phase == "break":
            total_time = int(self.break_time_entry.get()) * 60
        elif self.current_phase == "longbreak":
            total_time = int(self.longbreak_time_entry.get()) * 60

        elapsed = total_time - self.time_remaining
        self.time_elapsed_label.config(text=f"Time Elapsed: {elapsed // 60:02}:{elapsed % 60:02}")
        self.progress_bar["value"] = (elapsed / total_time) * 100

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_job = self.root.after(1000, self._run_timer)
        else:
            self._finish_session()

    def pause_timer(self):
        if self.state != "running":
            return

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.state = "paused"
        self.status_label.config(text="Status: Paused")

    def stop_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.state = "idle"
        self.time_remaining = 0
        self.progress_bar["value"] = 0

        self.status_label.config(text="Status: Stopped")
        self.time_left_label.config(text="Time Left: 00:00")
        self.time_elapsed_label.config(text="Time Elapsed: 00:00")

        self.current_iteration = 0
        self.total_iterations = 0

        self.current_phase = "work"
        self.phase_label.config(text="Phase: -")
        self.iterations_left_label.config(text="Iterations Left: -")

    def _finish_session(self):
        self.timer_job = None

        if self.current_phase == "work":
            self.current_iteration += 1

            if self.current_iteration >= self.total_iterations:
                self.current_phase = "longbreak"
            else:
                self.current_phase = "break"

        elif self.current_phase in ("break", "longbreak"):
            if self.current_iteration >= self.total_iterations:
                self.status_label.config(text="Pomodoro is Finished")
                self.state = "idle"
                return
            else:
                self.current_phase = "work"

        self._set_phase_timer()
        self._run_timer()

    def _set_phase_timer(self):
        if self.current_phase == "work":
            self.time_remaining = int(self.work_time_entry.get()) * 60
            self.phase_label.config(text="Phase: Work")
        elif self.current_phase == "break":
            self.time_remaining = int(self.break_time_entry.get()) * 60
            self.phase_label.config(text="Phase: Short Break")
        elif self.current_phase == "longbreak":
            self.time_remaining = int(self.longbreak_time_entry.get()) * 60
            self.phase_label.config(text="Phase: Long Break")

        self.progress_bar["value"] = 0
        self.time_elapsed_label.config(text="Time Elapsed: 00:00")
        self.time_left_label.config(text="Time Left: 00:00")
        self.iterations_left_label.config(text=f"Iterations Left: {self.total_iterations - self.current_iteration}")

class LayoutManager:
    def __init__(self, interface: PomodoroInterface):
        self.interface = interface
        self.root = self.interface.root

    def init_layout(self):
        self._time_entry_frame()
        self._buttons_frame()
        self._status_frame()        
        self._progress_bar_frame()

    def _time_entry_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)
        
        row1 = ttk.Frame(frame)
        row1.pack(pady=3)

        work_label = ttk.Label(row1, text="Work (mins):")
        work_label.pack(side="left", padx=3)

        self.interface.work_time_entry = ttk.Entry(row1, width=3)
        self.interface.work_time_entry.insert(0, "25")
        self.interface.work_time_entry.pack(side="left", padx=3)

        break_label = ttk.Label(row1, text="Break (mins):")
        break_label.pack(side="left", padx=3)

        self.interface.break_time_entry = ttk.Entry(row1, width=3)
        self.interface.break_time_entry.insert(0, "5")
        self.interface.break_time_entry.pack(side="left", padx=1)

        row2 = ttk.Frame(frame)
        row2.pack(pady=3)

        longbreak_label = ttk.Label(row2, text="Longbreak (mins):")
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

    def _status_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)

        self.interface.status_label = ttk.Label(frame, text="Status: Ready")
        self.interface.status_label.pack(pady=1)

        self.interface.phase_label = ttk.Label(frame, text="Phase: Work")
        self.interface.phase_label.pack(pady=1)

        self.interface.time_elapsed_label = ttk.Label(frame, text="Time Elapsed: 00:00")
        self.interface.time_elapsed_label.pack(pady=1)

        self.interface.time_left_label = ttk.Label(frame, text="Time Left: 00:00")
        self.interface.time_left_label.pack(pady=1)

        self.interface.iterations_left_label = ttk.Label(frame, text="Iterations Left: -")
        self.interface.iterations_left_label.pack(pady=1)

    def _progress_bar_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=1)

        self.interface.progress_bar = ttk.Progressbar(frame,
        orient="horizontal", length=225, mode="determinate")
        self.interface.progress_bar.pack(pady=1)

def run():
    root = tk.Tk()

    root.title("Pomodoro")
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"275x250+{(screen_width - 275) // 2}+{(screen_height - 250) // 2}")

    app = PomodoroInterface(root)

    root.mainloop()

if __name__ == "__main__":
    run()
