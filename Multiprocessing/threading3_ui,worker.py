# One UI thread (Tkinter) + one worker thread (tasks); shows task progress
import threading, queue, random, time, tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root, tasks):
        self.root = root
        self.tasks = tasks
        self.q = queue.Queue()
        self.worker_started = False

        root.title("Threaded Task Runner")
        root.geometry("560x380")

        ttk.Label(root, text="Task Progress", font=("TkDefaultFont", 14, "bold")).pack(pady=10)

        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True, padx=12)

        self.rows = []
        for i, name in enumerate(tasks):
            row = ttk.Frame(self.container)
            row.pack(fill="x", pady=4)
            lbl = ttk.Label(row, text=f"{i+1}. {name}", width=22, anchor="w")
            lbl.pack(side="left")
            bar = ttk.Progressbar(row, length=320, mode="determinate", maximum=100)
            bar.pack(side="left", padx=8)
            status = ttk.Label(row, text="waiting")
            status.pack(side="left")
            self.rows.append((bar, status))

        btns = ttk.Frame(root)
        btns.pack(pady=8)
        self.start_btn = ttk.Button(btns, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=4)
        ttk.Button(btns, text="Quit", command=root.destroy).pack(side="left", padx=4)

        # Poll UI queue
        self.root.after(50, self.process_queue)

    def start(self):
        if self.worker_started:
            return
        self.worker_started = True
        self.start_btn.state(["disabled"])
        threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        for i, name in enumerate(self.tasks):
            self.q.put(("status", i, "running"))
            progress = 0
            while progress < 100:
                time.sleep(random.uniform(0.05, 0.2))  # simulate work
                progress += random.randint(3, 12)
                self.q.put(("progress", i, min(progress, 100)))
            self.q.put(("status", i, "done ✓"))
        self.q.put(("all_done", None, None))

    def process_queue(self):
        try:
            while True:
                cmd, idx, val = self.q.get_nowait()
                if cmd == "progress":
                    bar, status = self.rows[idx]
                    bar["value"] = val
                elif cmd == "status":
                    bar, status = self.rows[idx]
                    status.config(text=val)
                elif cmd == "all_done":
                    self.start_btn.config(text="Done")
        except queue.Empty:
            pass
        self.root.after(50, self.process_queue)

if __name__ == "__main__":
    tasks = [f"Task {i}" for i in range(1, 9)]
    root = tk.Tk()
    App(root, tasks)
    root.mainloop()
