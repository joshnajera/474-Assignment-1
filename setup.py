import cx_Freeze
from cx_Freeze import setup, Executable
setup(name='lc2event', options= { "build_exe": {"packages":["sys","copy","itertools"]}}, version='0.1'\
, description='Cnvt lc to events', executables=[Executable("assignment1.py")])