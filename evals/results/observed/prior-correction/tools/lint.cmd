@echo off
rem Choose one interpreter; a lint failure must never trigger a second run.
where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 "%~dp0lint.py" %*
exit /b %errorlevel%
:use_python
python "%~dp0lint.py" %*
exit /b %errorlevel%
