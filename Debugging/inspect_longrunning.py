import os
import time
from pathlib import Path

counter = 0

Path("inspect_longrunning.pid").write_text(f"{os.getpid()}\n")

while True:
    counter += 1
    time.sleep(1)
