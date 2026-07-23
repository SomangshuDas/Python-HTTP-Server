@echo off
setlocal enabledelayedexpansion

rem Build script for Python HTTP Server.
rem Run this from inside the build_tools folder.
rem Produces dist\Python_HTTP_Server.exe via PyInstaller.

set "pyinstallerPath="
for /f "delims=" %%i in ('where pyinstaller 2^>nul') do (
    set "pyinstallerPath=%%i"
)

if not defined pyinstallerPath (
    echo PyInstaller not found in PATH. Install it with: pip install pyinstaller
    exit /b
)

set "srcFile=..\src\python_http_server.py"
set "icoFile=..\assets\python_http_server.ico"

if not exist "%srcFile%" (
    echo Could not find %srcFile%
    exit /b
)

"!pyinstallerPath!" --onefile --console --name "Python_HTTP_Server" --icon="%icoFile%" --distpath "..\dist" --workpath ".\build" --specpath "." "%srcFile%"

endlocal
