@echo off
:: Use the directory of this batch file to locate the Python script
set pythonScriptPath=%~dp0mainscript.py

:: Check if any files were dragged/dropped
if "%~1"=="" (
    echo No input files provided. Drag and drop one or more files onto this script.
    pause
    exit /b
)

:: Check if the Python script exists
if not exist "%pythonScriptPath%" (
    echo Python script not found: %pythonScriptPath%
    pause
    exit /b
)

:: Run the Python script and pass all the arguments (the dragged files)
python "%pythonScriptPath%" %*

:: Pause for output, if needed
pause
