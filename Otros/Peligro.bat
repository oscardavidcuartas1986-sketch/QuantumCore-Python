
jhonatan David Acosta Cardenas

@echo off
title Menu de Opciones

:inicio
cls
echo ********************
echo *****-=[MI MENU]=-*****
echo ********************
echo 1) Opcion 1  *** Abrir Google Chrome  
echo 2) Opcion 2  *Crear una carpeta nueva en el Escritorio 
echo 3) Opcion 3  *** Abrir Bloc de notas  
echo 4) Opcion 4  *Abrir Configuraci�n de Red  
echo 5) Opcion 5  * No abrir. Genera alto riesgo  
echo ********************
echo 6) Salir
echo ********************
echo.

set /p var=Seleccione una opcion [1-6]: 
if "%var%"=="1" goto op1
if "%var%"=="2" goto op2
if "%var%"=="3" goto op3
if "%var%"=="4" goto op4
if "%var%"=="5" goto op5
if "%var%"=="6" goto salir

::Mensaje de error, validaci�n cuando se selecciona una opci�n fuera de rango
echo. El numero "%var%" no es una opcion valida, por favor intente de nuevo.
echo.
pause
echo.
goto inicio

:op1
    echo.
    echo. Has elegido la opcion No. 1
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        start chrome
    echo.
    pause 
    goto inicio

:op2
    echo.
    echo. Has elegido la opcion No. 2
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        cd %USERPROFILE%\Desktop
        mkdir NuevaCarpeta
    echo.
    pause
    goto inicio

:op3
    echo.
    echo. Has elegido la opcion No. 3
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        start notepad
    echo.
    pause
    goto inicio
    
:op4
    echo.
    echo. Has elegido la opcion No. 4
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        start ms-settings:network
    echo.
    pause
    goto inicio

:op5
    echo.
    echo. Has elegido la opcion No. 5
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        :inicio1

      echo MsgBox "CIERRA ESTO SI PUEDES.", 64, "PERDER�S TODA LA       INFORMACI�N" >%temp%\mensaje.vbs
      start %temp%\mensaje.vbs 
   goto inicio1
    echo.
    pause
    goto inicio1

:salir
    @cls&exit

   