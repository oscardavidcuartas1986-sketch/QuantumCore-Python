@echo off 
title Selecciona un color

:inicio
cls
echo ********************
echo *****-=[trabajo de mierda]=-*****
echo ********************
echo 1) Opcion 1  *** Abrir programas basicos   
echo 2) Opcion 2  *Cerrar programas basicos  
echo 3) Opcion 3  *** Abrir programas ofimaticos  
echo 4) Opcion 4  *Cerrar programas ofimaticos  
echo 5) Opcion 5  * Lo mejor es no presionar la opcion 5... Te lo advierto  
echo 6) Opcion 6  *entrar al ceipa
echo ********************
echo 7) Salir
echo ********************
echo.

set /p var=Seleccione una opcion [1-7]: 
if "%var%"=="1" goto op1
if "%var%"=="2" goto op2
if "%var%"=="3" goto op3
if "%var%"=="4" goto op4
if "%var%"=="5" goto op5
if "%var%"=="6" goto op6
if "%var%"=="7" goto salir

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
        color 08
	start MSPAINT
	start NOTEPAD
	start WORDPAD
	start CHARMAP

    echo.
    pause 
    goto inicio

:op2
    echo.
    echo. Has elegido la opcion No. 2
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        color 09
	taskkill /im MSPAINT.EXE /F
	taskkill /im NOTEPAD.EXE /F
	taskkill /im WORDPAD.EXE /F
	taskkill /im CHARMAP.EXE /F
    echo.
    pause
    goto inicio

:op3
    echo.
    echo. Has elegido la opcion No. 3
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        color 0A
	start WINWORD
	start EXCEL
	start POWERPNT
	start ONENOTE
    echo.
    pause
    goto inicio
    
:op4
    echo.
    echo. Has elegido la opcion No. 4
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        color 0B
	taskkill /im WINWORD.EXE /F
	taskkill /im EXCEL.EXE /F
	taskkill /im POWERPNT.EXE /F
	taskkill /im ONENOTE.EXE /F
    echo.
    pause
    goto inicio

:op5
    echo.
    echo. Has elegido la opcion No. 5
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        color 0C
	start http://itm201526.webnode.es/fotogaleria/#imagen-terror-jpg2
	
	:op6
    echo.
    echo. Has elegido la opcion No. 6
    echo.
        ::Aqu� van las l�neas de comando de tu opci�n
        color 0C
	start https://ceipaeduco.sharepoint.com/sites/UBFlex/_layouts/15/Authenticate.aspx?Source=%2Fsites%2FUBFlex

    echo.
    pause
    goto inicio

:salir
    @cls&exit