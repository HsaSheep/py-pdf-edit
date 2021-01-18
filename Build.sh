#!/usr/bin/env bash

### 1File
#$pyinstaller Test.py --onefile
### No Console
#$ pyinstaller Test.py --noconsole
### EXE Name
#$ pyinstaller --name TEST-EXE-NAME Test.py
### Icon
#$ pyinstaller --icon=32x32.ico Test.py

pyinstaller --onefile --icon=32x32.ico --name PyPDF-Edit_TESTBUILD main.py
# pyinstaller --onefile --icon=32x32.ico Serial2BLEKeyboard.spec