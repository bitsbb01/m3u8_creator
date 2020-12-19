@echo off

setlocal

set BATCH_DIR=%~dp0
set PROJ_MAIN_DIR=%BATCH_DIR%..\..
set MODULE_PATH=%PROJ_MAIN_DIR%\ez_m3u8_creator

pushd "%PROJ_MAIN_DIR%"
rem Exclusion via config file currently not working in bandit 1.6.2
bandit -r "%MODULE_PATH%" --exclude "ez_m3u8_creator/tests/,ez_m3u8_creator/pricefinderapp/tests/"
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Issues Found
    goto exit_ok
) else (
    echo *** Some Issues Found
    goto exit_error
)

:exit_error
popd
endlocal
exit /B 1

:exit_ok
popd
endlocal
exit /B 0
