# One UI thread (Tkinter) + multiple worker threads; shows task progress
import threading, queue, random, time, tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root, tasks, num_workers=3):
        self.root = root
        self.tasks = tasks
        self.num_workers = num_workers
        self.q = queue.Queue()
        self.task_queue = queue.Queue()
        self.workers_started = False
        self.completed_tasks = 0

        root.title(f"Threaded Task Runner ({num_workers} workers)")
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
            bar = ttk.Progressbar(row, length=250, mode="determinate", maximum=100)
            bar.pack(side="left", padx=8)
            status = ttk.Label(row, text="waiting", width=12)
            status.pack(side="left")
            worker_lbl = ttk.Label(row, text="", width=10, foreground="blue")
            worker_lbl.pack(side="left")
            self.rows.append((bar, status, worker_lbl))

        btns = ttk.Frame(root)
        btns.pack(pady=8)
        self.start_btn = ttk.Button(btns, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=4)
        ttk.Button(btns, text="Quit", command=root.destroy).pack(side="left", padx=4)

        # Poll UI queue
        self.root.after(50, self.process_queue)

    def start(self):
        if self.workers_started:
            return
        self.workers_started = True
        self.start_btn.state(["disabled"])
        
        # Add all tasks to the task queue
        for i in range(len(self.tasks)):
            self.task_queue.put(i)
        
        # Start worker threads
        for worker_id in range(self.num_workers):
            threading.Thread(target=self.worker, args=(worker_id,), daemon=True).start()

    def worker(self, worker_id):
        worker_name = f"W{worker_id + 1}"
        while True:
            try:
                task_idx = self.task_queue.get(timeout=0.1)
            except queue.Empty:
                break
            
            # Show which worker is handling this task
            self.q.put(("worker", task_idx, worker_name))
            self.q.put(("status", task_idx, "running"))
            
            progress = 0
            while progress < 100:
                time.sleep(random.uniform(0.05, 0.2))  # simulate work
                progress += random.randint(3, 12)
                self.q.put(("progress", task_idx, min(progress, 100)))
            
            self.q.put(("status", task_idx, "done ✓"))
            self.q.put(("worker", task_idx, ""))
            self.q.put(("task_done", None, None))
            self.task_queue.task_done()

    def process_queue(self):
        try:
            while True:
                cmd, idx, val = self.q.get_nowait()
                if cmd == "progress":
                    bar, status, worker_lbl = self.rows[idx]
                    bar["value"] = val
                elif cmd == "status":
                    bar, status, worker_lbl = self.rows[idx]
                    status.config(text=val)
                elif cmd == "worker":
                    bar, status, worker_lbl = self.rows[idx]
                    worker_lbl.config(text=val)
                elif cmd == "task_done":
                    self.completed_tasks += 1
                    if self.completed_tasks >= len(self.tasks):
                        self.start_btn.config(text="All Done!", state="normal")
        except queue.Empty:
            pass
        self.root.after(50, self.process_queue)

if __name__ == "__main__":
    tasks = [f"Task {i}" for i in range(1, 9)]
    root = tk.Tk()
    App(root, tasks, num_workers=3)  # 3 worker threads
    root.mainloop()
