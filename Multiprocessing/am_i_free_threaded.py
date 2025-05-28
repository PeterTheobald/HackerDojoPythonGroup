import sysconfig
if sysconfig.get_config_var("Py_GIL_DISABLED"):
    print('I am running free-threaded Python (faster)')
else:
    print('I am running GIL locked Python (slower)')
