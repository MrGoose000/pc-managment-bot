@echo off
echo Set WshShell = CreateObject("WScript.Shell") >%TEMP%\tmp.vbs
echo WshShell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Run\MyBat", "%~dp0start1.bat", "REG_SZ" >>%TEMP%\tmp.vbs
echo WshShell.Run "regedit /s %TEMP%\tmp.vbs", 0, True >>%TEMP%\tmp.vbs
cscript /nologo %TEMP%\tmp.vbs
del %TEMP%\tmp.vbs
exit
