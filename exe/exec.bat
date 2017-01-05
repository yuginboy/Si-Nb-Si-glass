cd %~dp0
echo "start simulation"
echo %~dp0
start "C:\Program Files\SESSA V2.0\bin\sessa.exe" /c 
ping 127.0.0.1 -n 7 > nul
%~dp0run.exe "PROJECT LOAD SESSION %~dp0load.ses"
ping 127.0.0.1 -n 2 > nul
REM Taskkill /IM sessa.exe /F
exit










