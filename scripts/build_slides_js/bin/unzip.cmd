@echo off
if "%~1"=="-Z1" (
  C:\Windows\System32\tar.exe -tf "%~2"
  exit /b %errorlevel%
)
if "%~1"=="-p" (
  C:\Windows\System32\tar.exe -xOf "%~2" "%~3"
  exit /b %errorlevel%
)
exit /b 2
