@echo off

rem the safety module throws a Unicode error on Travis, so we need a base version

safety check --bare
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Issues Found
    exit /B 0
) else (
    echo *** Some safety Issues found, run full safety check
    exit /B 1
)
