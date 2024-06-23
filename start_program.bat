@echo off
REM Debugging-Informationen anzeigen
echo Aktivieren der virtuellen Umgebung...

REM Pfad zur virtuellen Umgebung
set VENV_PATH="%~dp0venv"

REM Aktivieren der virtuellen Umgebung
call %VENV_PATH%\Scripts\activate.bat

REM Überprüfen, ob die Aktivierung erfolgreich war
if "%errorlevel%" neq "0" (
    echo Fehler beim Aktivieren der virtuellen Umgebung.
    pause
    exit /b %errorlevel%
)

REM Debugging-Informationen anzeigen
echo Virtuelle Umgebung erfolgreich aktiviert.
echo Starten des Python-Skripts...

REM Starten des Python-Skripts
python "%~dp0main.py"

REM Überprüfen, ob das Python-Skript erfolgreich ausgeführt wurde
if "%errorlevel%" neq "0" (
    echo Fehler beim Ausführen des Python-Skripts.
    pause
    exit /b %errorlevel%
)

REM Debugging-Informationen anzeigen
echo Python-Skript erfolgreich ausgeführt.

REM Deaktivieren der virtuellen Umgebung
deactivate

REM Überprüfen, ob die Deaktivierung erfolgreich war
if "%errorlevel%" neq "0" (
    echo Fehler beim Deaktivieren der virtuellen Umgebung.
    pause
    exit /b %errorlevel%
)

REM Debugging-Informationen anzeigen
echo Virtuelle Umgebung erfolgreich deaktiviert.

pause
