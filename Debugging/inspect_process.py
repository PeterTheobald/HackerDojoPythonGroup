# inspect_process.py
import sys
from pathlib import Path

pid = int(Path("inspect_longrunning.pid").read_text().strip())

Path("inspect_process_helper.py").write_text("""
import __main__
print("Attached successfully")
print("counter =", getattr(__main__, "counter", None))
""")

# Note: must run as root,
# or allow same-user process attach permission w `sudo sysctl kernel.yama.ptrace_scope=0`
sys.remote_exec(pid, "inspect_process_helper.py")
