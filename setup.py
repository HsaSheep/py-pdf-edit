# BUILD : python setup.py bdist_msi

import sys
from cx_Freeze import setup, Executable

TARGET_FILE = "main.py"
EXE_FILE_NAME = "PyPDF-Edit"
EXE_VER = "0.01"
EXE_NAME_VER = EXE_FILE_NAME+" "+EXE_VER

# build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
#
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"
#
# setup(
#         name=EXE_FILE_NAME,
#         version=EXE_VER,
#         description=EXE_FILE_NAME+" "+EXE_VER,
#         options={"build_exe": build_exe_options},
#         executables=[Executable(TARGET_FILE, icon="32x32.ico", base=base)]
# )

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

exe = Executable(
        script=TARGET_FILE,
        base=base,
        icon="32x32.ico",
)

setup(
        name=EXE_FILE_NAME,
        version=EXE_VER,
        description=EXE_NAME_VER,
        executables=[exe]
)
