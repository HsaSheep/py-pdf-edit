@echo off

cd /d %~dp0

makensis.exe setup_nsis.nsi

pause
exit