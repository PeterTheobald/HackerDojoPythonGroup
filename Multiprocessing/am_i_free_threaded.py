import sysconfig
import sys

v=sys.version
if sysconfig.get_config_var("Py_GIL_DISABLED"):
    print(f'I am running free-threaded Python (faster), version {v}')
else:
    print(f'I am running GIL locked Python (slower) version {v}')
