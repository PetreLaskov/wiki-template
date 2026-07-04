@echo off
rem Knowledge Compiler lint — Windows wrapper. Run from the repo root.
where py >nul 2>nul && (py -3 "%~dp0lint.py" %*) || (python "%~dp0lint.py" %*)
