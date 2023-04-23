# BUILD : python setup.py bdist_msi

import sys
from cx_Freeze import setup, Executable

import values

TARGET_FILE = "tkinter_main.py"
EXE_FILE_NAME = values.EXE_FILE_NAME
EXE_VER = values.EXE_VER
EXE_NAME_VER = values.EXE_NAME_VER

base = None

# コンソール非表示 #
if sys.platform == "win32":
    base = "Win32GUI"

buildOption = dict(
    include_files=["32x32.ico"]
)

setup(
    name=EXE_FILE_NAME,
    version=EXE_VER,
    description="PDF Marge, Split, Rotate and Convert IMG Tool.",
    options=dict(build_exe=buildOption),
                 executables=[
                     Executable(target_name=EXE_FILE_NAME,
                                script=TARGET_FILE,
                                base=base,
                                icon="32x32.ico"
                                )
                ]
)
